local TurtlePresence = CreateFrame("Frame")
TurtlePresence:RegisterEvent("PLAYER_ENTERING_WORLD")
TurtlePresence:RegisterEvent("ZONE_CHANGED")
TurtlePresence:RegisterEvent("ZONE_CHANGED_NEW_AREA")
TurtlePresence:RegisterEvent("PLAYER_LEVEL_UP")
TurtlePresence:RegisterEvent("PLAYER_XP_UPDATE")

local lastPresenceData = ""

local function ternary(condition, T, F)
    if cond then
        return T
    else
        return F
    end
end

local function getPlayerData(event, arg1) 
    return {
        name = UnitName("player"), 
        realm = GetRealmName(), 
        class = UnitClass("player"), 
        zone = GetZoneText(), 
        subzone = GetSubZoneText(), 
        race = UnitRace("player"), 
        level = ternary(event == "PLAYER_LEVEL_UP", arg1, UnitLevel("player")),
    }
end

local function serializePlayerData(playerData)
    return string.format(
        "name=%s\nrealm=%s\nclass=%s\nzone=%s\nlevel=%d\nrace=%s\nsubzone=%s",
        playerData.name, playerData.realm, playerData.class, playerData.zone,
        playerData.level, playerData.race, playerData.subzone
    )
end

local function printDebugInfo(playerData)
    DEFAULT_CHAT_FRAME:AddMessage(serializePlayerData(playerData))
end

local function updatePresenceData(playerData)
    local fileContent = serializePlayerData(playerData)

    if fileContent ~= lastPresenceData then
        -- SuperWoW feature - export to game directory/Imports/TurtlePresenceData.txt
        ExportFile("TurtlePresenceData", fileContent)
        lastPresenceData = fileContent
    end
end

local function onEvent(self, event, arg1, ...)
    local playerData = getPlayerData(event, arg1)
    -- printDebugInfo(playerData)
    updatePresenceData(playerData)
end

TurtlePresence:SetScript("OnEvent", onEvent)
