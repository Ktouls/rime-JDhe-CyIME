-- 无输入状态按 ` 正常进入简单鹤反查；
-- 已有编码输入状态按 ` 直接切换实时拆分开关 (chaifen: 不拆 / 扌斥)
local kAccepted = 1
local kNoop = 2

local M = {}

function M.func(key_event, env)
    if key_event:release() or key_event:ctrl() or key_event:alt() or key_event:super() then
        return kNoop
    end
    if key_event.keycode == 96 then -- '`' (grave)
        local ctx = env.engine.context
        local inp = ctx.input
        if inp ~= "" and inp:sub(1, 1) ~= "`" and inp:sub(1, 3) ~= "oiz" then
            local cur = ctx:get_option("chaifen")
            ctx:set_option("chaifen", not cur)
            if ctx.refresh_non_confirmed_composition then
                ctx:refresh_non_confirmed_composition()
            end
            return kAccepted
        end
    end
    return kNoop
end

return M
