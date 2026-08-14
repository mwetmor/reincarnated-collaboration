/*
	
	GRIM DAWN SURVIVAL MODE
	
	For more information, visit us at http://www.grimdawn.com
	
*/

gd.survival.eventControl = {}


--
-- Controls for the Survival Mode event.
-- start and end Wave Tiers
-- check failure state
-- check finished state
-- check whether event is active
--

-- Event NPC Ids, to control whether they can be interacted with while the event is active, to prevent accidental clicking.
local EventNPCIds = {0, 0, 0, 0, 0, 0, 0}

-- Reward Tiers occur every 10 waves, up to 200 waves
local rewardTier = 0

-- Check in the case that players tried for the next reward tier, but failed. This results in Compensation loot rather than the full loot
local eventFailed = false

local eventFinished = false
local eventLoaded = false
local eventRestarted = false
local checkpoint = false

-- player spawn point Coords, also used to spawn Constitution at the end of a tier
local spawnPointCoords = nil
local constitutionRefillEntity = nil


--
-- Spawn Beacons
-- Spawn Beacons accelerate monster movement in their spawn areas
--
local spawnBeaconIds = {0, 0, 0, 0, 0, 0}
local spawnBeaconCoords = {nil, nil, nil, nil, nil}
local spawnBeaconSpawned = {false, false, false, false, false}

function gd.survival.eventControl.spawnBeacon01OnAddToWorld(objectId)
	if Server then
		spawnBeaconCoords[1] = Entity.Get(objectId):GetCoords()
		local spawn = nil

		if not spawnBeaconSpawned[1] then
			spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
			spawn:SetCoords(spawnBeaconCoords[1])
			spawnBeaconIds[1] = spawn:GetId()
			spawnBeaconSpawned[1] = true

		end
	
	end

end

function gd.survival.eventControl.spawnBeacon02OnAddToWorld(objectId)
	if Server then
		spawnBeaconCoords[2] = Entity.Get(objectId):GetCoords()
		local spawn = nil

		if not spawnBeaconSpawned[2] then
			spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
			spawn:SetCoords(spawnBeaconCoords[2])
			spawnBeaconIds[2] = spawn:GetId()
			spawnBeaconSpawned[2] = true

		end
	
	end

end

function gd.survival.eventControl.spawnBeacon03OnAddToWorld(objectId)
	if Server then
		spawnBeaconCoords[3] = Entity.Get(objectId):GetCoords()
		local spawn = nil

		if not spawnBeaconSpawned[3] then
			spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
			spawn:SetCoords(spawnBeaconCoords[3])
			spawnBeaconIds[3] = spawn:GetId()
			spawnBeaconSpawned[3] = true

		end
	
	end

end

function gd.survival.eventControl.spawnBeacon04OnAddToWorld(objectId)
	if Server then
		spawnBeaconCoords[4] = Entity.Get(objectId):GetCoords()
		local spawn = nil

		if not spawnBeaconSpawned[4] then
			spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
			spawn:SetCoords(spawnBeaconCoords[4])
			spawnBeaconIds[4] = spawn:GetId()
			spawnBeaconSpawned[4] = true

		end
	
	end

end

function gd.survival.eventControl.spawnBeacon05OnAddToWorld(objectId)
	if Server then
		spawnBeaconCoords[5] = Entity.Get(objectId):GetCoords()
		local spawn = nil

		if not spawnBeaconSpawned[5] then
			spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
			spawn:SetCoords(spawnBeaconCoords[5])
			spawnBeaconIds[5] = spawn:GetId()
			spawnBeaconSpawned[5] = true

		end
	
	end

end

--
-- NPC Control
--
local eventNPCCoords = nil
local merchantNPCCoords = nil

-- Event NPC
-- Spawn different versions of Event NPC based on event state
-- give out inventor tokens to all players
local inventorTokensGranted = false

function gd.survival.eventControl.NPCTokensGlobalMP()
	GiveTokenToLocalPlayer("DISMANTLING_UNLOCKED")
	GiveTokenToLocalPlayer("CONVERTING_UNLOCKED")

end


function gd.survival.eventControl.eventNPCScriptEntityOnAddToWorld(objectId)
	if Server then
		eventNPCCoords = Entity.Get(objectId):GetCoords()
		local spawn = nil
		
		local wave = Game.GetSurvivalWaveTier()

		if wave == 0 then
			spawn = Entity.Create ("records/creatures/npcs/npc_event_01.dbr")
		elseif eventFailed || eventFinished then
			spawn = Entity.Create ("records/creatures/npcs/npc_event_03.dbr")
		else
			spawn = Entity.Create ("records/creatures/npcs/npc_event_02.dbr")
		end

		spawn:SetCoords(eventNPCCoords)
		
		if not inventorTokensGranted then
			inventorTokensGranted = true
			GiveTokenToLocalPlayer("DISMANTLING_UNLOCKED")
			GiveTokenToLocalPlayer("CONVERTING_UNLOCKED")
			LuaGlobalEvent("grantInventorTokensGlobalMP")
		
		end
	
	end

end

-- Swap Event NPC to new state
function gd.survival.eventControl.swapEventEntity()
	if Server then
		local wave = Game.GetSurvivalWaveTier()
		local spawn = Entity.Get(EventNPCIds[1])
		
		spawn:Destroy()

		if ((wave == 0 || eventRestarted) && checkpoint == false) then
			spawn = Entity.Create ("records/creatures/npcs/npc_event_01.dbr")
			eventRestarted = false
		elseif eventFailed || eventFinished then
			spawn = Entity.Create ("records/creatures/npcs/npc_event_03.dbr")
		else
			spawn = Entity.Create ("records/creatures/npcs/npc_event_02.dbr")
		end

		spawn:SetCoords(eventNPCCoords)
	
	end

end

function gd.survival.eventControl.eventNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[1] = objectId
		
		if not eventLoaded then
			eventLoaded = true
			Game.AddObjective("tagNotification_Start")
		end
	
	end

end

function gd.survival.eventControl.smithNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[2] = objectId
	
	end

end

function gd.survival.eventControl.caravanNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[3] = objectId
	
	end

end

function gd.survival.eventControl.inventorNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[4] = objectId
	
	end

end

function gd.survival.eventControl.merchantNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[5] = objectId
	
	end

end

function gd.survival.eventControl.merchantNPCScriptEntityOnAddToWorld(objectId)
	if Server then
		merchantNPCCoords = Entity.Get(objectId):GetCoords()
		local spawn = Entity.Create ("records/creatures/npcs/merchants/merchants01.dbr")
		spawn:SetCoords(merchantNPCCoords)
	
	end

end

function gd.survival.eventControl.reallocatorNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[6] = objectId
	
	end

end

function gd.survival.eventControl.powerupsNPCOnAddToWorld(objectId)
	if Server then
		EventNPCIds[7] = objectId
	
	end

end


-- Check the current reward tier based on wave reached.
function gd.survival.eventControl.updateRewardTierGlobalMP()

	local wave = Game.GetSurvivalWaveTier()
	rewardTier = math.floor(wave / 10)

end

function gd.survival.eventControl.checkRewardTierGlobalMP()
	
	return rewardTier

end

function gd.survival.eventControl.checkRewardTier()

	local wave = Game.GetSurvivalWaveTier()
	rewardTier = math.floor(wave / 10)
	
	return rewardTier

end


-- If the players fail a wave, the event ends and reduced loot is awarded.
function gd.survival.eventControl.eventFailedGlobalMP()

	eventFailed = true
	
end

function gd.survival.eventControl.eventFailed()
	if Server then
		eventFailed = true
		
		LuaGlobalEvent("eventFailed")
	
	end

end

function gd.survival.eventControl.checkEventFailed()

	return eventFailed

end

-- Sets the event to finished so loot can be dispensed and no more enemies are spawned.
function gd.survival.eventControl.eventFinishedGlobalMP()

	eventFinished = true
	Game.UnlockTutorial(63)
	
end

function gd.survival.eventControl.eventFinished()
	if Server then
		
		eventFinished = true
		
		LuaGlobalEvent("eventFinished")
		
		-- Swap Event NPC to End State
		gd.survival.eventControl.swapEventEntity()
		
		-- Open treasure room and dispense rewards
		gd.survival.rewards.dispenseReward()
		print "event finished"
	
	end

end

-- Make sure event is not already active when cashing out
function gd.survival.eventControl.eventFinishedCashOut()
	if Server then
		if not eventActive then
			eventFinished = true
			
			LuaGlobalEvent("eventFinished")
			
			-- Swap Event NPC to End State
			gd.survival.eventControl.swapEventEntity()
			
			-- Open treasure room and dispense rewards
			gd.survival.rewards.dispenseReward()
			print "event finished"
		
		end
	
	end

end

function gd.survival.eventControl.checkEventFinished()

	return eventFinished

end


-- Checks for whether event is in progress. During event, NPCs and Defense Points cannot be interacted with
-- Activate and Deactive the Event, including NPCs
local eventActive = false

function gd.survival.eventControl.activateEventGlobalMP()

	eventActive = true
	
end

function gd.survival.eventControl.deactivateEventGlobalMP()

	eventActive = false
	
end

function gd.survival.eventControl.activateEvent()
	if Server then
		eventActive = true
		
		LuaGlobalEvent("activateEvent")
		
		-- disable defense sites and event NPC from being targetable
		Game.AllowNpcTalk(false)
		
	end

end

function gd.survival.eventControl.deactivateEvent()
	if Server then
		eventActive = false
		
		LuaGlobalEvent("deactivateEvent")
		
		-- enable defense sites and event NPC for conversation
		Game.AllowNpcTalk(true)
		
		-- Respawn Merchant to refresh wares based on player level
		local spawn = Entity.Get(EventNPCIds[5])
		spawn:Destroy()
		spawn = Entity.Create ("records/creatures/npcs/merchants/merchants01.dbr")
		spawn:SetCoords(merchantNPCCoords)
		
		-- Spawn Constitution Regen Item, Destroy previous one if still present
		if constitutionRefillEntity != nil then
			constitutionRefillEntity:Destroy()
			constitutionRefillEntity = nil
		end
		
		constitutionRefillEntity = Entity.Create ("records/items/misc/potions/potion_constitutionc01.dbr")
		constitutionRefillEntity:SetCoords(spawnPointCoords)
	
	end

end

function gd.survival.eventControl.eventStatus()

	return eventActive

end


-- Notify Mutators
function gd.survival.eventControl.notifyMutatorsGlobalMP()

	Game.NotifyNewMutators(false)

end

function gd.survival.eventControl.notifyMutatorsPluralGlobalMP()

	Game.NotifyNewMutators(true)

end

-- Start Event based on tier
function gd.survival.eventControl.startSurvivalModeEvent()

	local wave = Game.GetSurvivalWaveTier()
	rewardTier = math.floor(wave / 10)

	if rewardTier == 0 then
		gd.survival.tier01Waves.startSurvivalModeEvent()
	elseif rewardTier == 1 then
		gd.survival.tier02Waves.startSurvivalModeEvent()
	elseif rewardTier == 2 then
		gd.survival.tier03Waves.startSurvivalModeEvent()
	elseif rewardTier == 3 then
		gd.survival.tier04Waves.startSurvivalModeEvent()
	elseif rewardTier == 4 then
		gd.survival.tier05Waves.startSurvivalModeEvent()
	elseif rewardTier == 5 then
		gd.survival.tier06Waves.startSurvivalModeEvent()
	elseif rewardTier == 6 then
		gd.survival.tier07Waves.startSurvivalModeEvent()
	elseif rewardTier == 7 then
		gd.survival.tier08Waves.startSurvivalModeEvent()
	elseif rewardTier == 8 then
		gd.survival.tier09Waves.startSurvivalModeEvent()
	elseif rewardTier == 9 then
		gd.survival.tier10Waves.startSurvivalModeEvent()
	elseif rewardTier == 10 then
		gd.survival.tier11Waves.startSurvivalModeEvent()
	elseif rewardTier == 11 then
		gd.survival.tier12Waves.startSurvivalModeEvent()
	elseif rewardTier == 12 then
		gd.survival.tier13Waves.startSurvivalModeEvent()
	elseif rewardTier == 13 then
		gd.survival.tier14Waves.startSurvivalModeEvent()
	elseif rewardTier == 14 then
		gd.survival.tier15Waves.startSurvivalModeEvent()
	end
	
	gd.survival.eventControl.swapEventEntity()

end

-- Start the Event at Wave 51
function gd.survival.eventControl.startTier05Event()

	if Server then
		
		Game.SetSurvivalWaveTier(51)
		Game.SetSurvivalDifficulty(51)
		
		gd.survival.rewards.checkpoint50Used()
		checkpointActivated(51)
		checkpoint = true
		gd.survival.eventControl.swapEventEntity()
		
		gd.survival.tier06Waves.startSurvivalModeEvent()

	end

end

-- Start the Event at Wave 101
function gd.survival.eventControl.startTier10Event()

	if Server then
		Game.SetSurvivalWaveTier(101)
		Game.SetSurvivalDifficulty(101)
		
		gd.survival.rewards.checkpoint100Used()
		checkpointActivated(101)
		checkpoint = true
		gd.survival.eventControl.swapEventEntity()
		
		gd.survival.tier11Waves.startSurvivalModeEvent()

	end

end

-- Initiate Event Cleanup for restarting from the first wave
local function resetPlayersGlobalMP()

	-- Reset Code End Variables
	Game.ResetSurvivalEvent()
	
	-- Teleport player to spawn area
	local player = Game.GetLocalPlayer()
	local playerCoords = player:GetCoords()
	
	local fx = Entity.Create("records/fx/ui/riftgatepersonalopen_fxpak.dbr")
	local endFx = Entity.Create("records/fx/ui/riftgatepersonalopen_fxpak.dbr")
	
	if (fx != nil) then
		fx:NetworkEnable()
		fx:SetCoords(playerCoords)
	end

	if (endFx != nil) then
		endFx:NetworkEnable()
		endFx:SetCoords(spawnPointCoords)
	end
	
	Player.Teleport(spawnPointCoords)

end

function gd.survival.eventControl.resetEventGlobalMP()

	-- Reset Local Variables
	eventFinished = false
	eventFailed = false
	rewardTier = 0
	
	-- reset code variables and teleport players
	resetPlayersGlobalMP()

end

local function resetEventControl()

	if Server then
		eventRestarted = true
		checkpoint = false
		
		-- Reset Reward Variables, Despawn Chests, Lock Door
		gd.survival.rewards.resetVariables()
		
		-- Reset Event NPC
		gd.survival.eventControl.swapEventEntity()
		
		-- Reset Objectives
		Game.ClearObjectives()
		Game.AddObjective("tagNotification_Start")
		
		-- Reset Spawn Beacons
		local spawnBeacons = table.getn(spawnBeaconIds)
		
		for id = 1, spawnBeacons do
			local spawn = Entity.Get(spawnBeaconIds[id])
			
			if spawnBeaconSpawned[id] then
				if spawn != nil then
					spawn:Destroy()
				end
				
				spawn = Entity.Create ("records/creatures/traps/spawnbeacon.dbr")
				spawn:SetCoords(spawnBeaconCoords[id])
				spawnBeaconIds[id] = spawn:GetId()
				
			end
		
		end
	
	end

end

function gd.survival.eventControl.resetEvent()

	if Server then
		LuaGlobalEvent("eventResetGlobalMP")
		
		-- Reset Restart Attempts
		Game.ResetSurvivalRestarts()
		
		-- Reset All Core Survival Mode Functions and Variables
		resetEventControl()
		
		-- Reset Defense Variables, Despawn Defenses, Respawn Defense NPCs
		gd.survival.defenses.resetVariables()
		
		-- Reset Bonus Chest and Upgraded Loot Variables
		gd.survival.rewards.resetLootVariables()
		gd.survival.rewards.resetRestartVariable()

	end
	
end

-- Restart the Event at a higher wave
function gd.survival.eventControl.checkRestartCounterGlobalMP()
	
	local test = Game.GetSurvivalRestarts()
	local wave = Game.GetSurvivalWaveTier()
	
	if wave < 50 then
		test = -1
	end
	
	return test

end

function gd.survival.eventControl.restartEventGlobalMP()
	-- Reset Local Variables
	eventFinished = false
	eventFailed = false
	rewardTier = 0
	
	-- reset code variables and teleport players
	resetPlayersGlobalMP()

end

function gd.survival.eventControl.restartEvent()

	if Server then
		if Game.GetSurvivalRestarts() < 3 then
			local wave = Game.GetSurvivalWaveTier()
			Game.IncrementSurvivalRestarts()
			eventRestarted = true
			
			LuaGlobalEvent("eventRestartGlobalMP")
			
			-- Reset All Core Survival Mode Functions and Variables
			resetEventControl()
			
			-- Set Rewards to Restart, reduced Tribute Gain
			gd.survival.rewards.restartUsed()

			if wave >= 50 then
				local startingWave = ((math.floor (wave / 10)) * 10) - 20
				
				if startingWave > 1 then
					Game.SetSurvivalWaveTier(startingWave)
					Game.SetSurvivalDifficulty(startingWave)
				
				end
				
				if startingWave > 80 then
					gd.survival.rewards.RestartTest(startingWave)
				
				end

			end
		
		end
	
	end

end


-- Teleport Player Out of Treasure Room
function gd.survival.eventControl.spawnPointOnAddToWorld(objectId)

	spawnPointCoords = Entity.Get(objectId):GetCoords()
	
end

function gd.survival.eventControl.teleportPlayer(triggererId)
	
	local test = gd.survival.eventControl.checkEventFinished()
	
	if not test then
		local player = Entity.Get(triggererId)
		local playerCoords = player:GetCoords()
		
		local fx = Entity.Create("records/fx/ui/riftgatepersonalopen_fxpak.dbr")
		local endFx = Entity.Create("records/fx/ui/riftgatepersonalopen_fxpak.dbr")
		
		if (fx != nil) then
			fx:NetworkEnable()
			fx:SetCoords(playerCoords)
		end

		if (endFx != nil) then
			endFx:NetworkEnable()
			endFx:SetCoords(spawnPointCoords)
		end
		
		Player.Teleport(spawnPointCoords)
	
	end

end


