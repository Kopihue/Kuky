local M = {
    plugins_path = vim.fn.stdpath("data")
}

M.update = function()
    print("Updating plugin")
end

M.install = function(plugin, config)
    local parts = {}
    for part in string.gmatch(plugin, "[^/]+") do
	table.insert(parts, part)
    end
    local plugin_name = parts[#parts]
    local plugin = "https://github.com/" .. plugin .. ".git"

    if not vim.uv.fs_stat(M.plugins_path .. "/" .. plugin_name) then
	vim.notify("Installing -> " .. plugin_name)
	local result = vim.fn.system({
	    "git",
	    "clone",
	    "--depth", "1",
	    "--filter=blob:none",
	    plugin,
	    M.plugins_path .. "/" .. plugin_name,
	})
    end

    vim.opt.rtp:prepend(M.plugins_path .. "/" .. plugin_name)
    config()
end

return M
