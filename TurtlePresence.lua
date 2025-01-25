local TurtlePresence = CreateFrame("Frame")
TurtlePresence:RegisterEvent("PLAYER_ENTERING_WORLD")
TurtlePresence:RegisterEvent("ZONE_CHANGED")
TurtlePresence:RegisterEvent("ZONE_CHANGED_NEW_AREA")
TurtlePresence:RegisterEvent("PLAYER_LEVEL_UP")
TurtlePresence:RegisterEvent("PLAYER_XP_UPDATE")

local function printDebugInfo(name, realm, class, zone, level, race, subzone)
    local debugMessage = string.format(
        "Debug Info: Name: %s - %s, Class: %s, Zone: %s, Level: %d, Race: %s, Subzone: %s",
        name, realm, class, zone, level, race, subzone
    )
    DEFAULT_CHAT_FRAME:AddMessage(debugMessage)
end

local function updatePresenceData(name, realm, class, zone, level, race, subzone)
    local fileContent = string.format(
        "name=%s\nrealm=%s\nclass=%s\nzone=%s\nlevel=%d\nrace=%s\nsubzone=%s",
        name, realm, class, zone, level, race, subzone
    )

    -- SuperWoW feature - export to game directory/Imports/TurtlePresenceData.txt
    ExportFile("TurtlePresenceData", fileContent)
end

local function onEvent(self, event, arg1, ...)
    local name = UnitName("player")
    local realm = GetRealmName()
    local class = UnitClass("player")
    local zone = GetZoneText()
    local subzone = GetSubZoneText()
    local race = UnitRace("player")
    local level = UnitLevel("player")

    if event == "PLAYER_LEVEL_UP" then
        level = arg1
    end

    -- printDebugInfo(name, realm, class, zone, level, race, subzone)
    updatePresenceData(name, realm, class, zone, level, race, subzone)
end

TurtlePresence:SetScript("OnEvent", onEvent)
