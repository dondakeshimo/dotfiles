local function yank_file_path(opts)
  local path = vim.fn.expand("%:.")
  local l1, l2

  if opts.range > 0 then
    l1 = opts.line1
    l2 = opts.line2
  else
    l1 = vim.fn.line("'<")
    l2 = vim.fn.line("'>")
  end

  local ref = (l1 == l2)
    and path .. ":L" .. l1
    or  path .. ":L" .. l1 .. "-L" .. l2

  vim.fn.setreg("0", ref)
  vim.fn.setreg("+", ref)
end

vim.api.nvim_create_user_command("YankFilePath", yank_file_path, {
  range = true,
})