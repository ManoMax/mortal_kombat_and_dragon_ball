-- Opt-in telemetry; invoked only through a temporary Common.Lua configuration.
-- Quick versus starts before external module discovery, so use Common.Lua.
if not dbzProbeFile then
    dbzProbeFile = assert(io.open(assert(os.getenv('DBZ_TRACE')), 'w'))
    dbzProbeTick = 0
end
local old = id()
dbzProbeTick = dbzProbeTick + 1
for p = 1, 2 do
    if player(p) then
        local read = _G.var or _G.varGet
        dbzProbeFile:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
            dbzProbeTick, p, roundNo(), roundState(), stateNo(), life(), read(20),
            numProj(), projHitTime(7100), projGuardedTime(7100), numExplod(7200)))
    end
end
dbzProbeFile:flush()
playerId(old)
loop()
