--[[

- Don't describe package's overview here as code comments, refer to each package's help page.
- Lazy setting is rough because enough comfortable speed now.

--]]

require("lazy").setup({
  spec = {
    {
      "nvim-treesitter/nvim-treesitter",
      build = ":TSUpdate",
      lazy = true,
      event = "BufRead",
      main = "nvim-treesitter.configs",
      opts = {
        highlight = { enable = true },
        ensure_installed = {
          "bash",
          "c",
          "comment",
          "diff",
          "go",
          "html",
          "java",
          "javascript",
          "json",
          "jsonc",
          "lua",
          "luadoc",
          "luap",
          "markdown",
          "markdown_inline",
          "printf",
          "python",
          "query",
          "regex",
          "rust",
          "sql",
          "toml",
          "tsx",
          "typescript",
          "vim",
          "vimdoc",
          "xml",
          "yaml",
        },
      },
    },
    {
      "nvim-treesitter/nvim-treesitter-context",
      dependencies = {
        "nvim-treesitter/nvim-treesitter",
      },
      lazy = true,
      event = "BufRead",
      ft = { "markdown" },
      opts = {
        on_attach = function(bufnr)
          local ft = vim.fn.getbufvar(bufnr, "&filetype")
          local ret = false
          if ft == "markdown" then
            ret = true
          end

          return ret
        end
      },
    },
    {
      "neovim/nvim-lspconfig",
      lazy = false,
      dependencies = {
        "williamboman/mason.nvim",
        "williamboman/mason-lspconfig.nvim",
        "hrsh7th/cmp-nvim-lsp",
        "nvim-telescope/telescope.nvim",
        "nvimdev/lspsaga.nvim",
      },
      config = function(_, _)
        vim.api.nvim_create_autocmd("LspAttach", {
          callback = function(_)
            local builtin = require("telescope.builtin")
            vim.keymap.set("n", "gd", vim.lsp.buf.definition, { buffer = true })
            vim.keymap.set("n", "K", "<cmd>Lspsaga hover_doc<CR>", { buffer = true })
            vim.keymap.set("n", "gi", builtin.lsp_implementations, { buffer = true })
            vim.keymap.set("n", "gn", "<cmd>Lspsaga rename<CR>", { buffer = true })
            vim.keymap.set("n", "ga", "<cmd>Lspsaga code_action<CR>", { buffer = true })
            vim.keymap.set("n", "gr", builtin.lsp_references, { buffer = true })
            vim.keymap.set("n", "gf", vim.lsp.buf.format, { buffer = true })
            vim.keymap.set("n", "[g", vim.diagnostic.goto_prev, { buffer = true })
            vim.keymap.set("n", "]g", vim.diagnostic.goto_next, { buffer = true })
          end,
        })
        vim.lsp.config('*', {
          capabilities = require('cmp_nvim_lsp').default_capabilities(
            vim.lsp.protocol.make_client_capabilities()
          ),
        })
        vim.lsp.config('terraformls', {
          capabilities = require('cmp_nvim_lsp').default_capabilities(
            vim.lsp.protocol.make_client_capabilities()
          ),
          offset_encoding = "utf-8",
        })
        vim.lsp.config('terraformls', {
          capabilities = require('cmp_nvim_lsp').default_capabilities(
            vim.lsp.protocol.make_client_capabilities()
          ),
          offset_encoding = "utf-8",
        })
        -- vacuum 用の設定
        vim.filetype.add {
          pattern = {
            ['openapi.*%.ya?ml'] = 'yaml.openapi',
            ['openapi.*%.json'] = 'json.openapi',
          },
        }
      end,
    },
    {
      'williamboman/mason.nvim',
      opts = {},
    },
    {
      "williamboman/mason-lspconfig.nvim",
      lazy = false,
      dependencies = {
        "williamboman/mason.nvim",
      },
      opts = {
        ensure_installed = {
          "gopls",
          "lua_ls",
          "rust_analyzer",
        },
      },
    },
    {
      "j-hui/fidget.nvim",
      lazy = true,
      event = "VeryLazy",
      opts = {},
    },
    {
      "nvimdev/lspsaga.nvim",
      lazy = true,
      event = "VeryLazy",
      opts = {
        code_action = {
          keys = {
            quit = "<Esc>",
          },
        },
        lightbulb = { enable = false },
        rename = {
          auto_save = true,
          project_max_witdh = 100,
          keys = {
            quit = "<C-c>"
          },
        },
      },
    },
    {
      'nvim-flutter/flutter-tools.nvim',
      lazy = false,
      dependencies = {
        'nvim-lua/plenary.nvim',
      },
      opts = {
        flutter_lookup_cmd = "asdf where flutter",
      },
    },
    {
      "hrsh7th/nvim-cmp",
      lazy = true,
      event = "InsertEnter",
      dependencies = {
        "hrsh7th/cmp-nvim-lsp",
        "hrsh7th/cmp-nvim-lsp-signature-help",
        "hrsh7th/cmp-nvim-lsp-document-symbol",
        "hrsh7th/cmp-buffer",
        "hrsh7th/cmp-path",
        "hrsh7th/cmp-cmdline",
        "L3MON4D3/LuaSnip",
        "saadparwaiz1/cmp_luasnip",
        "ray-x/cmp-treesitter",
        "onsails/lspkind.nvim",
        "zbirenbaum/copilot-cmp",
      },
      config = function(_, _)
        local cmp = require("cmp")
        local lspkind = require('lspkind')
        vim.keymap.set("i", "<C-n>", cmp.complete, {})
        vim.keymap.set("i", "<C-p>", cmp.complete, {})
        cmp.setup({
          snippet = {
            expand = function(args)
              require('luasnip').lsp_expand(args.body)
            end,
          },
          sources = {
            { name = "copilot" },
            { name = "nvim_lsp" },
            { name = "treesitter" },
            { name = "nvim_lsp_document_symbol" },
            { name = "nvim_lsp_signature_help" },
            { name = "buffer" },
            { name = "path" },
          },
          mapping = cmp.mapping.preset.insert({
            ["<C-p>"] = cmp.mapping.select_prev_item(),
            ["<C-n>"] = cmp.mapping.select_next_item(),
            ['<C-e>'] = cmp.mapping.abort(),
            ['<C-y>'] = cmp.mapping.confirm({ select = true }),
            ['<CR>'] = cmp.mapping.confirm({ select = false }),
          }),
          experimental = {
            ghost_text = true,
          },
          formatting = {
            format = lspkind.cmp_format({
              mode = 'symbol',
              maxwidth = 80,
              ellipsis_char = '...',
              symbol_map = { Copilot = "" },
              before = function(entry, vim_item)
                vim_item.menu = entry.source.name
                return vim_item
              end
            })
          },
        })
        cmp.setup.cmdline('/', {
          mapping = cmp.mapping.preset.cmdline(),
          sources = {
            { name = 'buffer' }
          }
        })
        cmp.setup.cmdline(':', {
          mapping = cmp.mapping.preset.cmdline(),
          sources = cmp.config.sources({
            { name = 'path' }
          }, {
            { name = 'cmdline' }
          }),
          matching = { disallow_symbol_nonprefix_matching = false }
        })
      end,
    },
    {
      "hrsh7th/cmp-nvim-lsp",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/cmp-nvim-lsp-signature-help",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/cmp-nvim-lsp-document-symbol",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/cmp-buffer",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/cmp-path",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/cmp-cmdline",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "L3MON4D3/LuaSnip",
      tag = "v1.1.0",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "saadparwaiz1/cmp_luasnip",
      lazy = true,
      event = "InsertEnter",
      dependencies = {
        "L3MON4D3/LuaSnip",
      },
    },
    {
      "ray-x/cmp-treesitter",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "onsails/lspkind.nvim",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "nvim-tree/nvim-web-devicons",
      lazy = true,
      event = "VeryLazy",
    },
    {
      "nvim-lualine/lualine.nvim",
      dependencies = {
        "nvim-tree/nvim-web-devicons",
      },
      lazy = true,
      event = "VeryLazy",
      opts = {
        options = {
          icons_enabled = true,
          theme = 'auto',
          component_separators = { left = '', right = '' },
          section_separators = { left = '', right = '' },
          disabled_filetypes = {
            statusline = {},
            winbar = {},
          },
          ignore_focus = {},
          always_divide_middle = true,
          globalstatus = false,
          refresh = {
            statusline = 1000,
            tabline = 1000,
            winbar = 1000,
          }
        },
        sections = {
          lualine_a = { 'mode' },
          lualine_b = { 'branch', 'diff', 'diagnostics' },
          lualine_c = { 'filename' },
          lualine_x = { 'encoding', 'fileformat', 'filetype' },
          lualine_y = { 'progress' },
          lualine_z = { 'location' }
        },
        inactive_sections = {
          lualine_a = {},
          lualine_b = {},
          lualine_c = { 'filename' },
          lualine_x = { 'location' },
          lualine_y = {},
          lualine_z = {}
        },
        tabline = {},
        winbar = {},
        inactive_winbar = {},
        extensions = {}
      },
    },
    {
      "nvim-telescope/telescope.nvim",
      dependencies = {
        "nvim-lua/plenary.nvim",
      },
      opts = {
        defaults = {
          layout_config = {
            prompt_position = "top",
          },
          sorting_strategy = "ascending",
        },
      },
      config = function(_, opts)
        require("telescope").setup(opts)
        local builtin = require("telescope.builtin")
        vim.keymap.set("n", "<leader>fp", builtin.git_files, {})
        vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
        vim.keymap.set("n", "<leader>fb", builtin.buffers, {})
        vim.keymap.set("n", "<leader>fh", builtin.help_tags, {})
        vim.keymap.set("n", "<leader>fr", builtin.resume, {})
        vim.keymap.set("n", "<leader>fj", builtin.jumplist, {})
        vim.keymap.set("n", "<leader>fl", builtin.loclist, {})
        vim.keymap.set("n", "<leader>fs", builtin.lsp_workspace_symbols, {})
        vim.keymap.set("n", "<leader>fx", builtin.diagnostics, {})
      end,
    },
    {
      "nvim-telescope/telescope-file-browser.nvim",
      dependencies = {
        "nvim-telescope/telescope.nvim",
        "nvim-lua/plenary.nvim",
      },
      config = function()
        require("telescope").load_extension("file_browser")
        vim.keymap.set("n", "<leader>ff", ":Telescope file_browser path=%:p:h select_buffer=true hidden=true<CR>")
        vim.keymap.set("n", "<leader>fd", ":Telescope file_browser hidden=true<CR>")
      end,
    },
    {
      "AckslD/nvim-neoclip.lua",
      dependencies = {
        { "kkharji/sqlite.lua", module = 'sqlite' },
        "nvim-telescope/telescope.nvim",
      },
      config = function()
        require("neoclip").setup({
          enable_persistent_history = true,
          keys = {
            telescope = {
              i = {
                paste = '<nop>',
                paste_behind = '<nop>',
              }
            }
          }
        })
        vim.keymap.set("n", "<leader>fy", ":Telescope neoclip unnamed extra=plus<cr>")
      end,
    },
    {
      "nvim-telescope/telescope-frecency.nvim",
      lazy = true,
      event = "VeryLazy",
      dependencies = { "kkharji/sqlite.lua" },
      config = function()
        require("telescope").load_extension("frecency")
      end,
    },
    {
      "nvim-lua/plenary.nvim",
      lazy = true,
      event = "VeryLazy",
    },
    {
      "kkharji/sqlite.lua",
      lazy = true,
      event = "VeryLazy",
    },
    {
      "MunifTanjim/nui.nvim",
      lazy = true,
      event = "VeryLazy",
    },
    {
      "machakann/vim-sandwich",
    },
    {
      'windwp/nvim-autopairs',
      event = "InsertEnter",
      opts = {},
    },
    {
      "lukas-reineke/indent-blankline.nvim",
      main = "ibl",
      opts = {},
    },
    {
      "lewis6991/gitsigns.nvim",
      opts = {
        on_attach = function(bufnr)
          local gitsigns = require('gitsigns')

          local function map(mode, l, r, opts)
            opts = opts or {}
            opts.buffer = bufnr
            vim.keymap.set(mode, l, r, opts)
          end

          -- Navigation
          map('n', ']c', function()
            if vim.wo.diff then
              vim.cmd.normal({ ']c', bang = true })
            else
              gitsigns.nav_hunk('next')
            end
          end)

          map('n', '[c', function()
            if vim.wo.diff then
              vim.cmd.normal({ '[c', bang = true })
            else
              gitsigns.nav_hunk('prev')
            end
          end)

          -- Actions
          map('n', '<leader>hs', gitsigns.stage_hunk)
          map('n', '<leader>hr', gitsigns.reset_hunk)
          map('v', '<leader>hs', function() gitsigns.stage_hunk { vim.fn.line('.'), vim.fn.line('v') } end)
          map('v', '<leader>hr', function() gitsigns.reset_hunk { vim.fn.line('.'), vim.fn.line('v') } end)
          map('n', '<leader>hS', gitsigns.stage_buffer)
          map('n', '<leader>hu', gitsigns.undo_stage_hunk)
          map('n', '<leader>hR', gitsigns.reset_buffer)
          map('n', '<leader>hp', gitsigns.preview_hunk)
          map('n', '<leader>hb', function() gitsigns.blame_line { full = true } end)
          map('n', '<leader>tb', gitsigns.toggle_current_line_blame)
          map('n', '<leader>hd', gitsigns.diffthis)
          map('n', '<leader>hD', function() gitsigns.diffthis('~') end)
          map('n', '<leader>hB', gitsigns.toggle_deleted)

          -- Text object
          map({ 'o', 'x' }, 'ih', ':<C-U>Gitsigns select_hunk<CR>')
        end,
      },
    },
    {
      "almo7aya/openingh.nvim",
      lazy = true,
      cmd = {
        "OpenInGHFile",
        "OpenInGHFileLines",
        "OpenInGHRepo",
      },
    },
    {
      "TimUntersberger/neogit",
      dependencies = "nvim-lua/plenary.nvim",
      lazy = true,
      keys = { "<leader>g" },
      cmd = "Neogit",
      config = function()
        require("neogit").setup({})
        vim.keymap.set("n", "<leader>g", ":Neogit<CR>", { silent = true, noremap = true })
      end,
    },
    {
      "junegunn/vim-easy-align",
      lazy = true,
      event = "InsertEnter",
      config = function()
        vim.keymap.set("x", "<leader>a", "<Plug>(EasyAlign)", { silent = true, noremap = true })
        vim.keymap.set("n", "<leader>a", "<Plug>(EasyAlign)", { silent = true, noremap = true })
      end,
    },
    {
      "zbirenbaum/copilot.lua",
      cmd = "Copilot",
      event = "InsertEnter",
      opts = {
        suggestion = { enabled = false },
        panel = { enabled = false },
        filetypes = {
          markdown = true,
          gitcommit = true,
        },
        copilot_model = 'gpt-4o-copilot',
      },
    },
    {
      'zbirenbaum/copilot-cmp',
      lazy = true,
      event = "InsertEnter",
      opts = {},
    },
    {
      "maxmx03/solarized.nvim",
      lazy = false,
      priority = 1000,
      opts = {},
      config = function(_, opts)
        vim.o.termguicolors = true
        vim.o.background = 'dark'
        require('solarized').setup(opts)
        vim.cmd.colorscheme 'solarized'
      end,
    },
    {
      "olimorris/codecompanion.nvim",
      dependencies = {
        "nvim-lua/plenary.nvim",
        "nvim-treesitter/nvim-treesitter",
        "j-hui/fidget.nvim",
        { 'echasnovski/mini.diff', opts = {} },
      },
      config = function()
        local default_model = "anthropic/claude-sonnet-4"

        require("fidget-spinner"):init()

        require("codecompanion").setup({
          strategies = {
            chat = {
              adapter = "openrouter",
              roles = {
                llm = function(adapter)
                  return "  CodeCompanion (" .. adapter.formatted_name .. ")"
                end,
                user = "  Me",
              },
              tools = {
                ["mcp"] = {
                  callback = function()
                    return require("mcphub.extensions.codecompanion")
                  end,
                  description = "Call tools and resources from the MCP Servers"
                }
              },
            },
            inline = {
              adapter = "openrouter",
            },
          },
          adapters = {
            openrouter = function()
              return require("codecompanion.adapters").extend("openai_compatible", {
                env = {
                  url = "https://openrouter.ai/api",
                  api_key = "OPENROUTER_API_KEY",
                  chat_url = "/v1/chat/completions",
                },
                schema = {
                  model = {
                    default = default_model,
                  },
                },
              })
            end,
          },
          opts = {
            language = "Japanese",
          },
          display = {
            chat = {
              show_header_separator = true,
              window = {
                position = "right",
              },
            },
            diff = {
              enabled = true,
              layout = "horizontal",
              provider = "mini_diff",
            },
          },
        })

        vim.keymap.set({ "n", "v" }, "<leader>ck", "<cmd>CodeCompanionActions<cr>", { noremap = true, silent = true })
        vim.keymap.set({ "n", "v" }, "<leader>cc", "<cmd>CodeCompanionChat Toggle<cr>", { noremap = true, silent = true })
        vim.keymap.set("v", "<leader>ca", "<cmd>CodeCompanionChat Add<cr>", { noremap = true, silent = true })
        -- Expand 'cc' into 'CodeCompanion' in the command line
        vim.cmd([[cab cc CodeCompanion]])
      end,
    },
    {
      "MeanderingProgrammer/render-markdown.nvim",
      dependencies = { "nvim-treesitter/nvim-treesitter", "echasnovski/mini.icons" },
      ft = { "markdown", "markdown.mdx", "Avante", "codecompanion" },
      opts = {
        file_types = { "markdown", "Avante", "codecompanion" },
      }
    },
    {
      "ravitemer/mcphub.nvim",
      dependencies = {
        "nvim-lua/plenary.nvim",
      },
      cmd = "MCPHub",
      build = "npm install -g mcp-hub@latest",
      config = function()
        require("mcphub").setup({
          extensions = {
            codecompanion = {
              show_result_in_chat = true,
              make_vars = true,
              make_slash_commands = true,
            }
          }
        })
      end,
    },
    {
      "mfussenegger/nvim-dap",
      lazy = true,
      config = function()
        vim.keymap.set({ "n" }, "<leader>dm", ":lua require'dap'.toggle_breakpoint()<CR>",
          { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>dc", ":lua require'dap'.continue()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>d]]", ":lua require'dap'.step_back()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>d]]", ":lua require'dap'.step_over()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>d}}", ":lua require'dap'.step_in()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>d{{", ":lua require'dap'.step_out()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>dq", ":lua require'dap'.terminate()<CR>", { noremap = true, silent = true })
      end,
    },
    {
      "rcarriga/nvim-dap-ui",
      dependencies = {
        "mfussenegger/nvim-dap",
        "nvim-neotest/nvim-nio",
      },
      config = function()
        vim.keymap.set("n", "<leader>du", ":lua require'dapui'.toggle()<CR>", { silent = true })

        local dap, dapui = require("dap"), require("dapui")

        dapui.setup()

        dap.listeners.before.attach.dapui_config = function()
          dapui.open()
        end
        dap.listeners.before.launch.dapui_config = function()
          dapui.open()
        end
        dap.listeners.before.event_terminated.dapui_config = function()
          dapui.close()
        end
        dap.listeners.before.event_exited.dapui_config = function()
          dapui.close()
        end
      end,
    },
    {
      "leoluz/nvim-dap-go",
      dependencies = {
        "rcarriga/nvim-dap-ui",
      },
      config = function(_, opts)
        require("dap-go").setup(opts)
        vim.keymap.set({ "n" }, "<leader>dt", ":lua require'dap-go'.debug_test()<CR>", { noremap = true, silent = true })
        vim.keymap.set({ "n" }, "<leader>dr", ":lua require'dap-go'.debug_test()<CR>", { noremap = true, silent = true })
      end,
    },
  },
  install = { colorscheme = { "solarized" } },
  checker = { enabled = true },
})
