vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
  pattern = "*.avsc",
  callback = function()
    vim.bo.filetype = "json"
  end,
})

-- detect files changed outside of nvim (e.g. by Claude Code) and reload the buffer.
-- autoread alone does not reload until something triggers a filesystem check,
-- so call :checktime on idle and focus events.
vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter", "CursorHold", "CursorHoldI", "TermClose", "TermLeave" }, {
  pattern = "*",
  callback = function()
    -- skip command-line window and unnamed/special buffers
    if vim.fn.mode() == "c" or vim.bo.buftype ~= "" then
      return
    end
    vim.cmd("checktime")
  end,
})
