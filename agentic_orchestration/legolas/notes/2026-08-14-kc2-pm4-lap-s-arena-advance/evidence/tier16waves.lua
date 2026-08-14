/*
	
	GRIM DAWN SURVIVAL MODE
	
	For more information, visit us at http://www.grimdawn.com
	
*/

gd.survival.tier16Waves = {}


-- Waves 151 through 160 for Survival Mode
-- At the end of the waves, the player has the option to stop the event and claim the treasure.
local survivalModeEventspawnPoint01Id = 0
local survivalModeEventEventStarted = false
local survivalModeEventEventKey = "SURVIVALMODE_EVENT16"


-- Possible Proxies for each wave and spawn point. If nil, then no proxies spawn from that spawn point for that wave. Randomly selected.
local spawnPoint01wave01Proxies = {"records/proxies/tier16waves/proxy_w01_p01a.dbr"}
local spawnPoint02wave01Proxies = {"records/proxies/tier16waves/proxy_w01_p02a.dbr"}
local spawnPoint03wave01Proxies = {"records/proxies/tier16waves/proxy_w01_p03a.dbr"}
local spawnPoint04wave01Proxies = {"records/proxies/tier16waves/proxy_w01_p04a.dbr"}
local spawnPoint05wave01Proxies = {"records/proxies/tier16waves/proxy_w01_p05a.dbr"}
local spawnPoint06wave01Proxies = {nil}

local spawnPoint01wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p01a.dbr"}
local spawnPoint02wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p02a.dbr"}
local spawnPoint03wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p03a.dbr"}
local spawnPoint04wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p04a.dbr"}
local spawnPoint05wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p05a.dbr"}
local spawnPoint06wave02Proxies = {"records/proxies/tier16waves/proxy_w02_p06a.dbr"}

local spawnPoint01wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p01a.dbr"}
local spawnPoint02wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p02a.dbr"}
local spawnPoint03wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p03a.dbr"}
local spawnPoint04wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p04a.dbr"}
local spawnPoint05wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p05a.dbr"}
local spawnPoint06wave03Proxies = {"records/proxies/tier16waves/proxy_w03_p06a.dbr"}

local spawnPoint01wave04Proxies = {"records/proxies/tier16waves/proxy_w04_p01a.dbr"}
local spawnPoint02wave04Proxies = {"records/proxies/tier16waves/proxy_w04_p02a.dbr"}
local spawnPoint03wave04Proxies = {"records/proxies/tier16waves/proxy_w04_p03a.dbr"}
local spawnPoint04wave04Proxies = {"records/proxies/tier16waves/proxy_w04_p04a.dbr"}
local spawnPoint05wave04Proxies = {nil}
local spawnPoint06wave04Proxies = {nil}

local spawnPoint01wave05Proxies = {"records/proxies/tier16waves/proxy_w05_p01a.dbr"}
local spawnPoint02wave05Proxies = {"records/proxies/tier16waves/proxy_w05_p02a.dbr"}
local spawnPoint03wave05Proxies = {"records/proxies/tier16waves/proxy_w05_p03a.dbr"}
local spawnPoint04wave05Proxies = {"records/proxies/tier16waves/proxy_w05_p04a.dbr"}
local spawnPoint05wave05Proxies = {nil}
local spawnPoint06wave05Proxies = {"records/proxies/tier16waves/proxy_w05_p06a.dbr"}

local spawnPoint01wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p01a.dbr"}
local spawnPoint02wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p02a.dbr"}
local spawnPoint03wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p03a.dbr"}
local spawnPoint04wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p04a.dbr"}
local spawnPoint05wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p05a.dbr"}
local spawnPoint06wave06Proxies = {"records/proxies/tier16waves/proxy_w06_p06a.dbr"}

local spawnPoint01wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p01a.dbr"}
local spawnPoint02wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p02a.dbr"}
local spawnPoint03wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p03a.dbr"}
local spawnPoint04wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p04a.dbr"}
local spawnPoint05wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p05a.dbr"}
local spawnPoint06wave07Proxies = {"records/proxies/tier16waves/proxy_w07_p06a.dbr"}

local spawnPoint01wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p01a.dbr"}
local spawnPoint02wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p02a.dbr"}
local spawnPoint03wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p03a.dbr"}
local spawnPoint04wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p04a.dbr"}
local spawnPoint05wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p05a.dbr"}
local spawnPoint06wave08Proxies = {"records/proxies/tier16waves/proxy_w08_p06a.dbr"}

local spawnPoint01wave09Proxies = {"records/proxies/tier16waves/proxy_w09_p01a.dbr"}
local spawnPoint02wave09Proxies = {"records/proxies/tier16waves/proxy_w09_p02a.dbr"}
local spawnPoint03wave09Proxies = {"records/proxies/tier16waves/proxy_w09_p03a.dbr"}
local spawnPoint04wave09Proxies = {"records/proxies/tier16waves/proxy_w09_p04a.dbr"}
local spawnPoint05wave09Proxies = {"records/proxies/tier16waves/proxy_w09_p05a.dbr"}
local spawnPoint06wave09Proxies = {nil}

local spawnPoint01wave10Proxies = {"records/proxies/tier16waves/proxy_w10_p01a.dbr"}
local spawnPoint02wave10Proxies = {"records/proxies/tier16waves/proxy_w10_p02a.dbr"}
local spawnPoint03wave10Proxies = {"records/proxies/tier16waves/proxy_w10_p03a.dbr"}
local spawnPoint04wave10Proxies = {"records/proxies/tier16waves/proxy_w10_p04a.dbr"}
local spawnPoint05wave10Proxies = {nil}
local spawnPoint06wave10Proxies = {"records/proxies/tier16waves/proxy_w10_p06a.dbr"}

-- Grant credit Token for defeating 150 waves
function gd.survival.tier16Waves.endsurvivalModeEvent(objectId)

	if Server then
		local eventFailed = gd.survival.eventControl.checkEventFailed()
		
		if not eventFailed then
			LuaGlobalEvent("completeProgressToken")
			LuaGlobalEvent("tier10ProgressToken")
			
		end
	
	end
	
end

local survivalModeEventParameters = { }
	survivalModeEventParameters.waves = { }
	survivalModeEventParameters.endCallback = gd.survival.tier16Waves.endsurvivalModeEvent
	survivalModeEventParameters.key = survivalModeEventEventKey
	survivalModeEventParameters.updatePeriod = 1000
	survivalModeEventParameters.patrolPoint = "PatrolPoint_Attack"
	

function gd.survival.tier16Waves.spawnPoint01OnAddToWorld(objectId)

	if Server then
		survivalModeEventspawnPoint01Id = objectId
		SurvivalEvent_OnAddToWorld(objectId, survivalModeEventEventKey)
	
	end

end

function gd.survival.tier16Waves.spawnPoint01OnRemoveFromWorld(objectId)

	if Server then
		SurvivalEvent_OnRemoveFromWorld(objectId)
	
	end
	
end

local function defineSpawnPoints01()

	survivalModeEventParameters.waves[1][1] = spawnPoint01wave01Proxies
	survivalModeEventParameters.waves[1][2] = spawnPoint01wave02Proxies
	survivalModeEventParameters.waves[1][3] = spawnPoint01wave03Proxies
	survivalModeEventParameters.waves[1][4] = spawnPoint01wave04Proxies
	survivalModeEventParameters.waves[1][5] = spawnPoint01wave05Proxies
	survivalModeEventParameters.waves[1][6] = spawnPoint01wave06Proxies
	survivalModeEventParameters.waves[1][7] = spawnPoint01wave07Proxies
	survivalModeEventParameters.waves[1][8] = spawnPoint01wave08Proxies
	survivalModeEventParameters.waves[1][9] = spawnPoint01wave09Proxies
	survivalModeEventParameters.waves[1][10] = spawnPoint01wave10Proxies

end

local function defineSpawnPoints02()
	
	survivalModeEventParameters.waves[2][1] = spawnPoint02wave01Proxies
	survivalModeEventParameters.waves[2][2] = spawnPoint02wave02Proxies
	survivalModeEventParameters.waves[2][3] = spawnPoint02wave03Proxies
	survivalModeEventParameters.waves[2][4] = spawnPoint02wave04Proxies
	survivalModeEventParameters.waves[2][5] = spawnPoint02wave05Proxies
	survivalModeEventParameters.waves[2][6] = spawnPoint02wave06Proxies
	survivalModeEventParameters.waves[2][7] = spawnPoint02wave07Proxies
	survivalModeEventParameters.waves[2][8] = spawnPoint02wave08Proxies
	survivalModeEventParameters.waves[2][9] = spawnPoint02wave09Proxies
	survivalModeEventParameters.waves[2][10] = spawnPoint02wave10Proxies

end

local function defineSpawnPoints03()
	
	survivalModeEventParameters.waves[3][1] = spawnPoint03wave01Proxies
	survivalModeEventParameters.waves[3][2] = spawnPoint03wave02Proxies
	survivalModeEventParameters.waves[3][3] = spawnPoint03wave03Proxies
	survivalModeEventParameters.waves[3][4] = spawnPoint03wave04Proxies
	survivalModeEventParameters.waves[3][5] = spawnPoint03wave05Proxies
	survivalModeEventParameters.waves[3][6] = spawnPoint03wave06Proxies
	survivalModeEventParameters.waves[3][7] = spawnPoint03wave07Proxies
	survivalModeEventParameters.waves[3][8] = spawnPoint03wave08Proxies
	survivalModeEventParameters.waves[3][9] = spawnPoint03wave09Proxies
	survivalModeEventParameters.waves[3][10] = spawnPoint03wave10Proxies
	
end

local function defineSpawnPoints04()

	survivalModeEventParameters.waves[4][1] = spawnPoint04wave01Proxies
	survivalModeEventParameters.waves[4][2] = spawnPoint04wave02Proxies
	survivalModeEventParameters.waves[4][3] = spawnPoint04wave03Proxies
	survivalModeEventParameters.waves[4][4] = spawnPoint04wave04Proxies
	survivalModeEventParameters.waves[4][5] = spawnPoint04wave05Proxies
	survivalModeEventParameters.waves[4][6] = spawnPoint04wave06Proxies
	survivalModeEventParameters.waves[4][7] = spawnPoint04wave07Proxies
	survivalModeEventParameters.waves[4][8] = spawnPoint04wave08Proxies
	survivalModeEventParameters.waves[4][9] = spawnPoint04wave09Proxies
	survivalModeEventParameters.waves[4][10] = spawnPoint04wave10Proxies
		
end

local function defineSpawnPoints05()
	
	survivalModeEventParameters.waves[5][1] = spawnPoint05wave01Proxies
	survivalModeEventParameters.waves[5][2] = spawnPoint05wave02Proxies
	survivalModeEventParameters.waves[5][3] = spawnPoint05wave03Proxies
	survivalModeEventParameters.waves[5][4] = spawnPoint05wave04Proxies
	survivalModeEventParameters.waves[5][5] = spawnPoint05wave05Proxies
	survivalModeEventParameters.waves[5][6] = spawnPoint05wave06Proxies
	survivalModeEventParameters.waves[5][7] = spawnPoint05wave07Proxies
	survivalModeEventParameters.waves[5][8] = spawnPoint05wave08Proxies
	survivalModeEventParameters.waves[5][9] = spawnPoint05wave09Proxies
	survivalModeEventParameters.waves[5][10] = spawnPoint05wave10Proxies
	
end

local function defineSpawnPoints06()
	
	survivalModeEventParameters.waves[6][1] = spawnPoint06wave01Proxies
	survivalModeEventParameters.waves[6][2] = spawnPoint06wave02Proxies
	survivalModeEventParameters.waves[6][3] = spawnPoint06wave03Proxies
	survivalModeEventParameters.waves[6][4] = spawnPoint06wave04Proxies
	survivalModeEventParameters.waves[6][5] = spawnPoint06wave05Proxies
	survivalModeEventParameters.waves[6][6] = spawnPoint06wave06Proxies
	survivalModeEventParameters.waves[6][7] = spawnPoint06wave07Proxies
	survivalModeEventParameters.waves[6][8] = spawnPoint06wave08Proxies
	survivalModeEventParameters.waves[6][9] = spawnPoint06wave09Proxies
	survivalModeEventParameters.waves[6][10] = spawnPoint06wave10Proxies
	
end

function gd.survival.tier16Waves.startSurvivalModeEvent()

	if Server then
		local eventFinished = gd.survival.eventControl.checkEventFinished()
		
		if not eventFinished then
			-- Initialize variables
			local spawnPointsTotal = numberOfSpawnPoints()
			
			for id = 1, spawnPointsTotal do
				survivalModeEventParameters.waves[id] = {}
			
			end
			
			-- Assign proxies to each spawn point for each wave
			defineSpawnPoints01()
			defineSpawnPoints02()
			defineSpawnPoints03()
			defineSpawnPoints04()
			defineSpawnPoints05()
			defineSpawnPoints06()
			
			
			SurvivalEvent_Start(survivalModeEventspawnPoint01Id, survivalModeEventParameters)
		
		end
		
	end

end
