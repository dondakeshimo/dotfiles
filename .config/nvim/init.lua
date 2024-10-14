--[[

- Top level configuration file (here) only invokes other files.
- Some options or keymaps depending on the plugin are set the plugin module.

--]]

require("bootstrap-lazy")
require("option")
require("keymap")
require("plugin") -- confirm that mapleader is set before invoke plugins
