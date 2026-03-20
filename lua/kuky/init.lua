local M = {
    plugins_path = vim.fn.stdpath("data")
}

M.install = function(plugin, config)
    local parts = {}
    for part in string.gmatch(plugin, "[^/]+") do
	table.insert(parts, part)
    end
    local plugin_name = parts[#parts]
    local plugin = "https://github.com/" .. plugin .. ".git"

    if not vim.uv.fs_stat(M.plugins_path .. "/" .. plugin_name) then
	print("Plugin doesn't exist")
    end
end

return M
