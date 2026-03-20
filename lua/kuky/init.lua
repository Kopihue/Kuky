local M = {
    plugins_path = vim.fn.stdpath("data")
}

M.hardupdates = function()
    os.execute("rm -rf " .. M.plugins_path .. "/*")
    print("Restart Neovim c':") end

M.check = function()
    local files = {}
    local handle = vim.loop.fs_scandir(M.plugins_path)
    while true do
	local name, t = vim.loop.fs_scandir_next(handle)
	if not name then break end
	table.insert(files, name)
    end

    for _, file in ipairs(files) do
	local plugin = M.plugins_path .. "/" .. file
	if vim.uv.fs_stat(plugin .. "/.git") then
	    print(file .. " Is a git repository")
	end
    end
end

M.install = function(plugin, config, dependencies)
    if dependencies then
	for _, dep in ipairs(dependencies) do
	    M.install(
		dep,
		function() end
	    )
	end
    end

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
