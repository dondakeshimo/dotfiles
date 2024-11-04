-- leader
vim.api.nvim_set_var("mapleader", " ")
vim.g.localmapleder = " "

-- emacs keybind on insert mode
vim.keymap.set("i", "<C-b>", "<Left>")
vim.keymap.set("i", "<C-f>", "<Right>")
vim.keymap.set("i", "<C-a>", "<C-o>^")
vim.keymap.set("i", "<C-e>", "<C-o>$")

-- scroll history at command line
vim.keymap.set("c", "<C-p>", "<Up>")
vim.keymap.set("c", "<C-n>", "<Down>")

-- ceterize screen when jump to next/prev search result
vim.keymap.set("n", "n", "nzz")
vim.keymap.set("n", "N", "Nzz")
vim.keymap.set("n", "*", "*zz")
vim.keymap.set("n", "#", "#zz")
