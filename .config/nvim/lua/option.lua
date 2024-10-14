-- user interface
vim.opt.ruler = true
vim.opt.number = true
vim.opt.title = true
vim.opt.ambiwidth  = "double"
vim.opt.list = true
vim.opt.signcolumn = "yes"
vim.opt.listchars = {
    tab = "»-",
    trail = "-",
    extends = "»",
    precedes = "«",
    nbsp = "%",
}

-- indent
vim.opt.autoindent = true
vim.opt.smartindent = true
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.tabstop = 2

-- cursor
vim.opt.whichwrap = "b,s,[,],<,>"
vim.opt.backspace = { "indent", "eol", "start" }
vim.opt.virtualedit = "block"
vim.opt.ttimeoutlen = 10

-- file manipulation
vim.opt.swapfile = false
vim.opt.hidden = true
vim.opt.wildmenu = true

-- interpretation number formats
vim.opt.nrformats = { "bin", "hex", "unsigned" }

-- searching options
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = true
vim.opt.incsearch = true
vim.opt.wrapscan = true

-- copy to global clipboard
vim.opt.clipboard = "unnamed"

-- updatetime
vim.opt.updatetime = 100

