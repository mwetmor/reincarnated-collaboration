/*
	
	GRIM DAWN SURVIVAL MODE
	
	For more information visit us at http://www.grimdawn.com
	
*/

--
-- Proxy based Survival Wave Event!
--
-- 'objectId' is the id of the ScriptEntity responsible for the event
-- 'params' is a table containing the following values
--     'waves'          - an array equal to number of spawn points. Each contains an array for the total number of waves which in turn have an array of Proxy dbrs to spawn from
--     'token'          - token to give at the end of the event [optional]
--     'updateCallback' - function called on each wave update   [optional]
--     'endCallback'    - function call at the end of the event [optional]
--     'updatePeriod'   - time between updates in milliseconds  [optional, default=1000ms]
--     'patrolPoint'    - patrol point group the spawns should head to upon spawning, set as a String [optional]
--		'key'				- the Unique Key string used to restore userdata in case the event is unloaded before it has concluded


-- if more spawn points added, need to update SurvivalEvent_Start accordingly
local survivalModeEventSpawnPoint02Id = 0
local survivalModeEventSpawnPoint03Id = 0
local survivalModeEventSpawnPoint04Id = 0
local survivalModeEventSpawnPoint05Id = 0
local survivalModeEventSpawnPoint06Id = 0

-- spawn data for randomized traps
local trapPointSpawned = {false, false, false, false, false, false, false, false}
local trapCoords = {nil, nil, nil, nil, nil, nil, nil, nil}
local trapObjects = {nil, nil, nil, nil, nil, nil, nil, nil}
local trapDbrs = {"records/creatures/traps/trap_a01.dbr",
"records/creatures/traps/trap_a02.dbr",
"records/creatures/traps/trap_a03.dbr",
"records/creatures/traps/trap_a04.dbr",
"records/creatures/traps/trap_a05.dbr",
"records/creatures/traps/trap_a06.dbr",
"records/creatures/traps/trap_a07.dbr",
"records/creatures/traps/trap_a08.dbr",
"records/creatures/traps/trap_a09.dbr",
"records/creatures/traps/trap_a10.dbr"}
local trapsInactive = false
local trapCooldown = 0

-- Random Master VO
local VOCooldown = 15
local VOFired = true
local VOChance = 250

-- if checkPoint is used, set to true to wave difficulty isn't increment again in MP
local checkpointUsed = false
local checkpointWave = 0

function checkpointActivated(waveNumber)
	if Server then
		checkpointUsed = true
		checkpointWave = waveNumber

	end
	
end


-- Additional Spawn Points beyond the first. If more than 5 exist, Tiers need to be updated with additional proxy assignments and Event_Start needs additional Entity initiations
function spawnPoint02OnAddToWorld(objectId)

	if Server then
		survivalModeEventSpawnPoint02Id = objectId
	
	end

end

function spawnPoint03OnAddToWorld(objectId)

	if Server then
		survivalModeEventSpawnPoint03Id = objectId
	
	end

end

function spawnPoint04OnAddToWorld(objectId)

	if Server then
		survivalModeEventSpawnPoint04Id = objectId
	
	end

end

function spawnPoint05OnAddToWorld(objectId)

	if Server then
		survivalModeEventSpawnPoint05Id = objectId
	
	end

end

function spawnPoint06OnAddToWorld(objectId)

	if Server then
		survivalModeEventSpawnPoint06Id = objectId
	
	end

end

-- Fixed at 6 Spawn Points, if more added, need to modify constant
local spawnPointsTotal = 6

function numberOfSpawnPoints()

	return spawnPointsTotal

end

-- Trap Spawn Locations. If more than 5 exist, need to update arrays.
function trapPoint01OnAddToWorld(objectId)

	if Server then
		trapCoords[1] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint02OnAddToWorld(objectId)

	if Server then
		trapCoords[2] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint03OnAddToWorld(objectId)

	if Server then
		trapCoords[3] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint04OnAddToWorld(objectId)

	if Server then
		trapCoords[4] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint05OnAddToWorld(objectId)

	if Server then
		trapCoords[5] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint06OnAddToWorld(objectId)

	if Server then
		trapCoords[6] = Entity.Get(objectId):GetCoords()

	end

end

function trapPoint07OnAddToWorld(objectId)

	if Server then
		trapCoords[7] = Entity.Get(objectId):GetCoords()
	
	end

end

function trapPoint08OnAddToWorld(objectId)

	if Server then
		trapCoords[8] = Entity.Get(objectId):GetCoords()		
	
	end

end

-- Define Mutator Pack List
-- Mutator Packs intended for players MUST have "player" in the dbr name. Otherwise it will get applied to the monsters.
local mutatorListMonsters = {"records/game/mutators/mutatorpak_monster_01.dbr",
"records/game/mutators/mutatorpak_monster_02.dbr",
"records/game/mutators/mutatorpak_monster_03.dbr",
"records/game/mutators/mutatorpak_monster_04.dbr",
"records/game/mutators/mutatorpak_monster_05.dbr",
"records/game/mutators/mutatorpak_monster_06.dbr",
"records/game/mutators/mutatorpak_monster_07.dbr",
"records/game/mutators/mutatorpak_monster_08.dbr",
"records/game/mutators/mutatorpak_monster_09.dbr",
"records/game/mutators/mutatorpak_monster_10.dbr",
"records/game/mutators/mutatorpak_monster_11.dbr",
"records/game/mutators/mutatorpak_monster_12.dbr",
"records/game/mutators/mutatorpak_monster_13.dbr",
"records/game/mutators/mutatorpak_monster_14.dbr",
"records/game/mutators/mutatorpak_monster_15.dbr",
"records/game/mutators/mutatorpak_monster_16.dbr",
"records/game/mutators/mutatorpak_monster_17.dbr"}

local mutatorListPlayer = {"records/game/mutators/mutatorpak_player_01.dbr",
"records/game/mutators/mutatorpak_player_02.dbr",
"records/game/mutators/mutatorpak_player_03.dbr",
"records/game/mutators/mutatorpak_player_04.dbr",
"records/game/mutators/mutatorpak_player_05.dbr",
"records/game/mutators/mutatorpak_player_06.dbr",
"records/game/mutators/mutatorpak_player_07.dbr",
"records/game/mutators/mutatorpak_player_08.dbr",
"records/game/mutators/mutatorpak_player_09.dbr",
"records/game/mutators/mutatorpak_player_10.dbr"}

-- Select Mutator(s) for the set of rounds
local function SurvivalEvent_MutatorRandomizer(mutatorCount)

	local totalMutatorsMonsters = table.getn(mutatorListMonsters)	
	local totalMutatorsPlayer = table.getn(mutatorListPlayer)
	local totalMutators = totalMutatorsMonsters + totalMutatorsPlayer
	
	local selectedList = {}
	
	print "selecting mutators"
	-- randomly select mutators until a unique list is created
	if mutatorCount <= totalMutators then
		math.randomseed(Time.Now())
		
		-- determine how many player vs monster mutators to roll
		local playerMutatorCount = 0
		local monsterMutatorCount = 0
		
		if mutatorCount >= 6 then
			playerMutatorCount = 2
		elseif mutatorCount >=2 then
			playerMutatorCount = 1
		end
		
		monsterMutatorCount = mutatorCount - playerMutatorCount
		if monsterMutatorCount < 0 then
			monsterMutatorCount = 0
		end
		
		-- roll player mutators until selected list is of size playerMutatorCount.
		if playerMutatorCount > 0 then
			while table.getn(selectedList) != playerMutatorCount do
				local rand = random(1,totalMutatorsPlayer)
				local found = false
				
				if rand < totalMutatorsPlayer then
					for id = 1, table.getn(selectedList) do
						if mutatorListPlayer[rand] == selectedList[id] then
							found = true
						
						end
					
					end
					
					if not found then
						table.insert(selectedList, mutatorListPlayer[rand])
					
					end
				
				end
			
			end
		
		end
		
		-- roll monster mutators untiul selected list is of size mutatorCount.
		if monsterMutatorCount > 0 then
			while table.getn(selectedList) != mutatorCount do
				local rand = random(1,totalMutatorsMonsters)
				local found = false
				
				if rand < totalMutatorsMonsters then
					for id = 1, table.getn(selectedList) do
						if mutatorListMonsters[rand] == selectedList[id] then
							found = true
						
						end
					
					end
					
					if not found then
						table.insert(selectedList, mutatorListMonsters[rand])
					
					end
				
				end
			
			end
			
		end
		
		-- Apply selected Mutators
		local totalMutatorsSelected = table.getn(selectedList)
		
		if totalMutatorsSelected > 1 then
			LuaGlobalEvent("notifyPluralMutators")
		else
			LuaGlobalEvent("notifyMutators")
		end
		
		
		for id = 1, totalMutatorsSelected do
			Game.AddMutator(selectedList[id])
		
		end		
	
	end

end

function SurvivalEvent_SelectMutators()

	local rewardTier = gd.survival.eventControl.checkRewardTier()
	local mutatorCount = 0
	
	-- if a checkpoint was used, override the tier, for MP purposes
	if checkpointWave > 0 then
		rewardTier = math.floor(checkpointWave / 10)
	end
	
	if rewardTier >= 17 then
		mutatorCount = 7
	elseif rewardTier >= 15 then
		mutatorCount = 6
	elseif rewardTier >= 13 then
		mutatorCount = 5
	elseif rewardTier >= 11 then
		mutatorCount = 4
	elseif rewardTier >= 9 then
		mutatorCount = 3
	elseif rewardTier >= 6 then
		mutatorCount = 2
	elseif rewardTier >= 3 then
		mutatorCount = 1
	else
		-- Play event start sound if no mutators selected
		Game.PlayNetSound("records/sounds/spak_eventbegin.dbr")
	end
	
	
	if mutatorCount > 0 then
		SurvivalEvent_MutatorRandomizer(mutatorCount)
		
	end

end


-- Start a wave event
function SurvivalEvent_Start(objectId, params)

	-- Set the Event as Active
	gd.survival.eventControl.activateEvent()
	
	-- define spawn point entities
	local entity = {}
	entity[1] = Entity.Get(objectId)
	entity[2] = Entity.Get(survivalModeEventSpawnPoint02Id)
	entity[3] = Entity.Get(survivalModeEventSpawnPoint03Id)
	entity[4] = Entity.Get(survivalModeEventSpawnPoint04Id)
	entity[5] = Entity.Get(survivalModeEventSpawnPoint05Id)
	-- final spawn point is for bonus spawns, player chooses to enable this
	entity[6] = Entity.Get(survivalModeEventSpawnPoint06Id)
	
	local userdata = Shared.getUserdata(objectid)
	
	if (userdata == nil) then
		userdata = {}
		Shared.setUserdata(objectId, userdata)
	end
	
	userdata.waveEvent = {}
	
	-- Setup waveEvent table in object userdata
	local waveEvent = userdata.waveEvent
	
	-- store # of spawn points
	waveEvent.numSpawns = table.getn(entity)
		
	-- define spawn points coordinates based on positions of spawn point entities
	waveEvent.coords = {}
	
	for id = 1, waveEvent.numSpawns do
		waveEvent.coords[id] =  entity[id]:GetCoords()
	
	end

	
	waveEvent.waveIndex = 0
	waveEvent.proxy = {}
	waveEvent.proxyKilled = {}
	waveEvent.waves = params.waves
	
	-- define number of waves for spawn point one, the main spawn point.
	waveEvent.numWaves = table.getn(waveEvent.waves[1])
	
	-- Define proxy and proxy kill check arrays
	for id = 1, waveEvent.numSpawns do
		waveEvent.proxy[id] = nil
		waveEvent.proxyKilled[id] = false
	
	end
	
	waveEvent.updateCallback = params.updateCallback or nil
	waveEvent.endCallback = params.endCallback or SurvivalEvent_DefaultEndCallback
	waveEvent.token = params.token or nil
	waveEvent.key = params.key
	waveEvent.updatePeriod = params.updatePeriod or 1000
	waveEvent.patrolPoint = params.patrolPoint or nil
	waveEvent.running = true
	
	-- Start receiving updates
	Script.RegisterForUpdate(objectId, "SurvivalEvent_Update", waveEvent.updatePeriod)
		
	-- Fire user start callback
	if (params.startCallback ~= nil) then
		params.startCallback(objectId)
	end
	
	-- Set Mutators
	SurvivalEvent_SelectMutators()
		
	-- Spawn first wave
	SurvivalEvent_SpawnNext(objectId)
	
	-- Update Objectives
	Game.ClearObjectives()
	Game.AddObjective("tagNotification_Active")
	
	-- Start Event on code end
	Game.StartSurvivalEvent()
	
	-- Reset Player Tier XP/Tribute Booleans
	LuaGlobalEvent("playerTierRewards")
	
end

-- Start Bonus Timer
function SurvivalEvent_StartBonusTimer()

	local tier = gd.survival.eventControl.checkRewardTier()
	
	-- if a checkpoint was used, override the tier, for MP purposes
	if checkpointWave > 0 then
		tier = math.floor(checkpointWave / 10)
	end
	
	local multiplier = Game.GetSurvivalMultiplier() 
	
	local defaultTimer = 0
	local tierBonus = 0
	
	if (Game.GetGameDifficulty() == Game.Difficulty.Normal) then
		defaultTimer = 75000
		tierBonus = 10000
	elseif (Game.GetGameDifficulty() == Game.Difficulty.Epic) then
		defaultTimer = 75000
		tierBonus = 11000
	else
		defaultTimer = 80000
		tierBonus = 12000
	end
	
	-- Default based on difficulty, adds time per reward tier, modified by current multiplier
	local timer = (1 / ((multiplier + 1) ^ 0.49)) * (defaultTimer + (tier * tierBonus))
	
	-- Set Bonus Timer (ms)
	Game.SetSurvivalTimer(timer)

end

local function SurvivalEvent_DespawnTraps()

	-- Despawn previous wave's traps, if any are active.
	local totalTraps = table.getn(trapCoords)
	
	if totalTraps > 0 then
		for id = 1, totalTraps do
			if trapObjects[id] != nil && trapPointSpawned[id] then
				trapPointSpawned[id] = false
				trapObjects[id]:Destroy()
				trapObjects[id] = nil
			end
		end
	end

end

function SurvivalEvent_SpawnNext(objectId)

	-- Increment the Survival Mode Difficulty AttributePak rank. This happens every wave.
	-- global monster stat modifier, stored in records/game/balancingadjustment_survivalmode_enemies01.dbr
	if checkpointUsed then
		checkpointUsed = false
	else
		Game.IncrementSurvivalDifficulty()
		
		-- Increment wave # on code end for score purposes
		Game.IncrementSurvivalWaveTier()
	end
	
	-- Respawn all players, then disable respawn for the wave
	Game.EnableRespawn()
	Game.DisableRespawn()
	
	--Begin Bonus Timer
	SurvivalEvent_StartBonusTimer()
	
	local waveEvent = Shared.getUserdata(objectId).waveEvent
	
	-- Spawn next proxy from each Spawn Point
	waveEvent.waveIndex = waveEvent.waveIndex + 1
	
	-- play wave end sound for the previous wave
	if waveEvent.waveIndex > 1 then
		Game.PlayNetSound("records/sounds/spak_waveend.dbr")
	
	end

	-- Check if final bonus spawn should be used
	local bonusSpawnStatus = gd.survival.rewards.checkBonusStatus()
	
	math.randomseed(Time.Now())
	
	for id = 1, waveEvent.numSpawns do
		if (waveEvent.waves[id][waveEvent.waveIndex] != nil && (id < waveEvent.numSpawns || bonusSpawnStatus == true)) then
			local totalProxies = table.getn(waveEvent.waves[id][waveEvent.waveIndex])
			
			-- select random proxy from the list
			local randomizer = random(1,totalProxies)
		
			if waveEvent.waves[id][waveEvent.waveIndex][randomizer] != nil then
				waveEvent.proxyKilled[id] = false
				waveEvent.proxy[id] = Proxy.Create(waveEvent.waves[id][waveEvent.waveIndex][randomizer], waveEvent.coords[id].origin, true) -- Proxy dbr, origin point, true for 'ignore boss spawn limit'
				waveEvent.proxy[id]:SetCoords(waveEvent.coords[id])

				-- set the spawns to patrol if a patrol point group was provided
				if waveEvent.proxy[id]:IsAmbush() == false && waveEvent.patrolPoint != nil then
					waveEvent.proxy[id]:LinkPatrolPointGroup(waveEvent.patrolPoint)
				
				end
				
				-- Execute the proxy to dispense monsters and follow the set path
				waveEvent.proxy[id]:Run()
			
			else
				waveEvent.proxyKilled[id] = true
				waveEvent.proxy[id] = nil
			end
		
		else
			waveEvent.proxyKilled[id] = true
			waveEvent.proxy[id] = nil
		end
	
	end
	
	-- Despawn previous wave's traps, if any are active.
	SurvivalEvent_DespawnTraps()
	
	-- Check to Spawn Random Traps
	local rand = random(1,100)
	local tier = gd.survival.eventControl.checkRewardTier()
	
	-- if a checkpoint was used, override the tier, for MP purposes
	if checkpointWave > 0 then
		tier = math.floor(checkpointWave / 10)
	end
	
	local test = 10 + tier * 1
	
	if rand <= test && tier >= 1 && not trapsInactive then
		local totalTraps = table.getn(trapCoords)
		local totalTrapDbrs = table.getn(trapDbrs)
		trapsInactive = true
		
		-- how many traps to spawn
		local trapSpawn = 0
		if tier < 5 && totalTraps >= 2 then
			trapSpawn = random(1, 3)
		elseif tier < 10 && totalTraps >= 4 then
			trapSpawn = random(1, 4)
		elseif totalTraps >= 6 then
			trapSpawn = random(1, 6)
		end
		
		if trapSpawn > 0 then
			-- trap level data
			local averageLevel = Game.GetAveragePlayerLevel()
			local trapLevel = ((averageLevel+(averageLevel/50))+1)
			
			for id = 1, trapSpawn do
				rand = random(1, totalTraps)
				
				if not trapPointSpawned[rand] then
					trapPointSpawned[rand] = true
				
					local randTrap = random(1, totalTrapDbrs)
					
					if trapDbrs[randTrap] != nil && trapCoords[rand] != nil  then
						trapObjects[rand] = Character.Create (trapDbrs[randTrap], trapLevel, nil)
						trapObjects[rand]:SetCoords(trapCoords[rand])
						
					end
					
				end
			
			end
		
		end
	
	elseif trapsInactive then
		trapCooldown = trapCooldown + 1
		
		if trapCooldown > 2 then
			trapCooldown = 0
			trapsInactive = false
		
		end
		
	end

	-- reset the checkpoint wave # to 0
	checkpointWave = 0
	
end

-- End the wave event
function SurvivalEvent_End(objectId)

	local waveEvent = Shared.getUserdata(objectId).waveEvent
	waveEvent.running = false

	-- Stop receiving updates
	Script.UnregisterForUpdate(objectId, "SurvivalEvent_Update")
	
	-- Sets the event to inactive
	gd.survival.eventControl.deactivateEvent()
	
	-- Reset Mutators
	Game.ResetMutators()
	
	-- Despawn Traps
	SurvivalEvent_DespawnTraps()
	
	-- Respawn Players
	Game.EnableRespawn()
	
	-- Update Reward Tier
	LuaGlobalEvent("updateRewardTier")
	
	-- End Event on code end
	Game.EndSurvivalEvent()
	
	-- Fire user end callback
	if (waveEvent.endCallback != nil) then
		waveEvent.endCallback(objectId)
	end
	
end

-- Update the wave event
function SurvivalEvent_Update(objectId)

	local waveEvent = Shared.getUserdata(objectId).waveEvent
	
	-- Fire user update callback
	if (waveEvent.updateCallback ~= nil) then
		waveEvent.updateCallback(objectId)
	end
	
	-- Chance to play Master's Taunts
	math.randomseed(Time.Now())
	local rand = random(1,VOChance)
	
	if rand == 1 && not VOFired then
		Game.PlayNetSound("records/sounds/npcdialogue/spak_master_taunts.dbr")
		VOFired = true
		VOChance = 250
	elseif VOFired then
		VOCooldown = VOCooldown + 1
	else
		VOChance = VOChance - 5
		if VOChance < 10 then
			VOChance = 10
		end
		
	end
	
	if VOCooldown >= 70 then
		VOFired = false
		VOCooldown = 0
	end
	
	-- Spawn next wave or end the event if the current waves have been killed
	-- If the event was failed, stop the event early
	local eventFailed = Game.PlayersDead()
	
	if not eventFailed then
		
		for id = 1, waveEvent.numSpawns do
			if (waveEvent.proxy[id] != nil && waveEvent.proxy[id]:AllKilled()) then
				waveEvent.proxyKilled[id] = true

			end
			
		end
		
		for id = 1, waveEvent.numSpawns do
			if (not waveEvent.proxyKilled[id]) then
				break
			end
			
			if id == waveEvent.numSpawns then
				if (waveEvent.waveIndex < waveEvent.numWaves) then
					for id = 1, waveEvent.numSpawns do
						waveEvent.proxyKilled[id] = false
						
					end
					
					print "starting next wave"
					SurvivalEvent_SpawnNext(objectId)
					
				else
					print "event successful"
					
					-- Play Success Event Sound
					Game.PlayNetSound("records/sounds/spak_eventend.dbr")
					
					-- Show Victory Screen Glow
					LuaGlobalEvent("screenGlow")
					
					-- Pause Bonus Timer
					Game.SetSurvivalTimer(0)
					
					-- Update Objectives
					Game.ClearObjectives()
					Game.AddObjective("tagNotification_Continue")
					
					-- Clean up
					SurvivalEvent_End(objectId)
					Game.KillAllMonsters()
					
					-- Grant XP and Tributes for finishing a tier
					LuaGlobalEvent("playerTierExperience")
					LuaGlobalEvent("playerTierTributes")

				end
				
			end
			
		end
	
	elseif not Game.IsHardcore() then
		print "event failed"
		gd.survival.eventControl.eventFailed()

		-- Play Failed Event Sound
		Game.PlayNetSound("records/sounds/spak_eventfail.dbr")
		
		-- Conclude the Event
		gd.survival.eventControl.eventFinished()
		
		-- Reset Bonus Timer
		Game.ResetSurvivalTimer()
		
		-- Clean up
		SurvivalEvent_End(objectId)
		Game.KillAllMonstersOnNextRespawn()
	
	end
	
end

-- Default end callback, called when the wave event ends
function SurvivalEvent_DefaultEndCallback(objectId)

	local waveEvent = Shared.getUserdata(objectId).waveEvent
	
	-- Give end token if set
	if (waveEvent.token ~= nil) then
		GiveTokenToLocalPlayer(waveEvent.token)
	end

end

-- Used to restore userdata in case the event is unloaded partway through
function SurvivalEvent_OnAddToWorld(objectId, key)

	Shared.restoreUserdata(objectId, key)
	
	local userdata = Shared.getUserdata(objectId)
	
	if (userdata != nil) then
		if (userdata.waveEvent.running) then
			Script.RegisterForUpdate(objectId, "SurvivalEvent_Update", userdata.waveEvent.updatePeriod)
			
		end
		
	end
	
end

function SurvivalEvent_OnRemoveFromWorld(objectId)

	local userdata = Shared.getUserdata(objectId)

	if (userdata != nil) then
		
		if (userdata.waveEvent.running) then
			Script.UnregisterForUpdate(objectId, "SurvivalEvent_Update")
			Shared.persistUserdata(objectId, userdata.waveEvent.key)
			
		else
			Shared.setUserdata(objectId, nil)
			
		end
		
	end
	
end

-- Randomly play VO when a Hero, Boss or Nemesis is killed
function SurvivalEvent_NemesisKill()
	
	if not VOFired then
		Game.PlayNetSound("records/sounds/npcdialogue/spak_master_compliments.dbr")
		VOFired = true
	end

end

function SurvivalEvent_BossKill()

	-- Chance to play Master's Compliments
	math.randomseed(Time.Now())
	local rand = random(1,6)
	
	if rand == 1 && not VOFired then
		Game.PlayNetSound("records/sounds/npcdialogue/spak_master_compliments.dbr")
		VOFired = true
	end

end

function SurvivalEvent_HeroKill()

	-- Chance to play Master's Compliments
	math.randomseed(Time.Now())
	local rand = random(1,20)
	
	if rand == 1 && not VOFired then
		Game.PlayNetSound("records/sounds/npcdialogue/spak_master_compliments.dbr")
		VOFired = true
	end

end

