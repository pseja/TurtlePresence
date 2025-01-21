local TurtlePresence = CreateFrame("Frame")
TurtlePresence:RegisterEvent("PLAYER_ENTERING_WORLD")
TurtlePresence:RegisterEvent("ZONE_CHANGED_NEW_AREA")
TurtlePresence:RegisterEvent("PLAYER_LEVEL_UP")

TurtlePresenceData = TurtlePresenceData or {}

local function printDebugInfo(name, realm, class, zone, level)
    local debugMessage = string.format(
        "Debug Info: Name: %s - %s, Class: %s, Zone: %s, Level: %d",
        name, realm, class, zone, level
    )
    DEFAULT_CHAT_FRAME:AddMessage(debugMessage)
end

local function updatePresenceData(name, realm, class, zone, level)
    TurtlePresenceData.name = name
    TurtlePresenceData.realm = realm
    TurtlePresenceData.class = class
    TurtlePresenceData.zone = zone
    TurtlePresenceData.level = level
end

local function onEvent(self, event, arg1, ...)
    local name = UnitName("player")
    local realm = GetRealmName()
    local class = UnitClass("player")
    local zone = GetZoneText()
    local level

    if event == "PLAYER_LEVEL_UP" then
        level = arg1 -- provided by level up event
    else
        level = UnitLevel("player") -- use current level for other events
    end

    printDebugInfo(name, realm, class, zone, level)
    updatePresenceData(name, realm, class, level, zone)
end

TurtlePresence:SetScript("OnEvent", onEvent)
