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
    },
    {
      "neovim/nvim-lspconfig",
      lazy = false,
      dependdencied = {
        "williamboman/mason.nvim",
        "williamboman/mason-lspconfig.nvim",
        "hrsh7th/cmp-nvim-lsp",
      },
      config = function(_, _)
        vim.api.nvim_create_autocmd("LspAttach", {
          callback = function(_)
            vim.keymap.set("n", "gd", vim.lsp.buf.definition, { buffer = true })
            vim.keymap.set("n", "K", vim.lsp.buf.hover, { buffer = true })
            vim.keymap.set("n", "gi", vim.lsp.buf.implementation, { buffer = true })
            vim.keymap.set("n", "gn", vim.lsp.buf.rename, { buffer = true })
            vim.keymap.set("n", "ga", vim.lsp.buf.code_action, { buffer = true })
            vim.keymap.set("n", "gr", vim.lsp.buf.references, { buffer = true })
            vim.keymap.set("n", "[g", vim.diagnostic.goto_prev, { buffer = true })
            vim.keymap.set("n", "]g", vim.diagnostic.goto_next, { buffer = true })
          end,
        })
        require("mason-lspconfig").setup_handlers({
          function(server_name)
            require("lspconfig")[server_name].setup({
              capabilities = require('cmp_nvim_lsp').default_capabilities(
              vim.lsp.protocol.make_client_capabilities()
              ),
            })
          end,
        })
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
      "folke/trouble.nvim",
      lazy = true,
      keys = { "<leader>xx", "<leader>xw", "<leader>xd", "<leader>xl", "<leader>xq", "gR" },
      config = function()
        require("trouble").setup({})
        vim.keymap.set("n", "<leader>xx", "<cmd>Trouble diagnostics<cr>", { silent = true, noremap = true })
      end,
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
        "hrsh7th/cmp-vsnip",
        "hrsh7th/vim-vsnip",
        "ray-x/cmp-treesitter",
        "onsails/lspkind.nvim",
      },
      config = function(_, _)
        local cmp = require("cmp")
        cmp.setup({
          snippet = {
            expand = function(args)
              vim.fn["vsnip#anonymous"](args.body)
            end,
          },
          sources = {
            { name = "nvim_lsp" },
            { name = "treesitter" },
            { name = "nvim_lsp_document_symbol" },
            { name = "buffer" },
            { name = "path" },
          },
          mapping = cmp.mapping.preset.insert({
            ["<C-p>"] = cmp.mapping.select_prev_item(),
            ["<C-n>"] = cmp.mapping.select_next_item(),
            ['<C-l>'] = cmp.mapping.complete(),
            ['<C-e>'] = cmp.mapping.abort(),
            ['<CR>'] = cmp.mapping.confirm({ select = false }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
          }),
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
      "hrsh7th/cmp-vsnip",
      lazy = true,
      event = "InsertEnter",
    },
    {
      "hrsh7th/vim-vsnip",
      lazy = true,
      event = "InsertEnter",
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
          component_separators = { left = '', right = ''},
          section_separators = { left = '', right = ''},
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
          lualine_a = {'mode'},
          lualine_b = {'branch', 'diff', 'diagnostics'},
          lualine_c = {'filename'},
          lualine_x = {'encoding', 'fileformat', 'filetype'},
          lualine_y = {'progress'},
          lualine_z = {'location'}
        },
        inactive_sections = {
          lualine_a = {},
          lualine_b = {},
          lualine_c = {'filename'},
          lualine_x = {'location'},
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
      lazy = true,
      keys = { "<leader>ff", "<leader>fg", "<leader>fb", "<leader>fh", "<leader>fr" },
      config = function()
        local builtin = require("telescope.builtin")
        vim.keymap.set("n", "<leader>ff", builtin.find_files, {})
        vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
        vim.keymap.set("n", "<leader>fb", builtin.buffers, {})
        vim.keymap.set("n", "<leader>fh", builtin.help_tags, {})
        vim.keymap.set("n", "<leader>fr", builtin.resume, {})
      end,
    },
    {
      "nvim-neo-tree/neo-tree.nvim",
      branch = "v3.x",
      dependencies = {
        "nvim-lua/plenary.nvim",
        "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
        "MunifTanjim/nui.nvim",
      },
      lazy = true,
      keys = { "<leader>t" },
      cmd = "Neotree",
      config = function()
        vim.keymap.set("n", "<leader>t", ":Neotree toggle<CR>", { silent = true, noremap = true })
      end,
    },
    {
      "nvim-lua/plenary.nvim",
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
      "Yggdroot/indentLine",
    },
    {
      "airblade/vim-gitgutter",
    },
    {
      "TimUntersberger/neogit",
      dependencies = "nvim-lua/plenary.nvim",
      lazy = true,
      cmd = "Neogit",
      opt = {},
    },
    {
      "github/copilot.vim",
      config = function()
        vim.api.nvim_set_var("copilot_filetypes", { "markdown" })
      end,
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
  },
  install = { colorscheme = { "solarized" } },
  checker = { enabled = true },
})
