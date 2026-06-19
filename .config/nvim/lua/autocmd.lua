vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
  pattern = "*.avsc",
  callback = function()
    vim.bo.filetype = "json"
  end,
})
