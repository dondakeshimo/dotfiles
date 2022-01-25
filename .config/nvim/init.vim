""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" init
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if &compatible
  set nocompatible
endif

set encoding=UTF-8
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" dein.vim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let s:dein_dir = expand('~/.config/nvim/bundles')
let s:dein_repo_dir = expand('~/.config/nvim/dein.vim')

" Install dein.vim if not exists
if &runtimepath !~# '/dein.vim'
  if !isdirectory(s:dein_repo_dir)
    execute '!git clone https://github.com/Shougo/dein.vim ' . fnamemodify(s:dein_repo_dir, ':p')
  endif
  execute 'set runtimepath^=' . fnamemodify(s:dein_repo_dir, ':p')
endif

if dein#load_state(s:dein_dir)
    call dein#begin(s:dein_dir)

    let s:toml = '~/.config/nvim/dein/dein.toml'
    let s:lazy_toml = '~/.config/nvim/dein/dein_lazy.toml'

    call dein#load_toml(s:toml, {'lazy': 0})
    call dein#load_toml(s:lazy_toml, {'lazy': 1})

    call dein#end()
    call dein#save_state()
endif

if has('vim_starting') && dein#check_install()
  call dein#install()
endif

filetype plugin indent on
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" vim options
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" user interface
set ruler
set number
set title
set ambiwidth=double
set list
set listchars=tab:»-,trail:-,extends:»,precedes:«,nbsp:%

" indent
set autoindent
set smartindent
set shiftwidth=4
set expandtab
set tabstop=4

" cursor
set whichwrap=b,s,[,],<,>
set backspace=indent,eol,start
set virtualedit=block
set ttimeoutlen=10

" file manipulation
set noswapfile
set backupdir=$HOME/.vimbackup
set hidden
set wildmenu

" interpretation number formats
set nrformats-=octal

" searching options
set ignorecase
set smartcase
set hlsearch
set incsearch
set wrapscan

" copy to global clipboard
set clipboard=unnamed

" updatetime
set updatetime=100
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" leader
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let mapleader = "\<space>"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" colorscheme
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set background=dark
colorscheme solarized
syntax enable
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" scroll history at command line
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
cnoremap <C-p> <Up>
cnoremap <C-n> <Down>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" emacs keybind on insert mode
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
inoremap <C-b> <Left>
inoremap <C-f> <Right>
inoremap <C-a> <C-o>^
inoremap <C-e> <C-o>$
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" visible multi byte space
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! ZenkakuSpace()
  highlight ZenkakuSpace cterm=underline ctermfg=lightblue guibg=darkgray
endfunction

if has('syntax')
  augroup ZenkakuSpace
    autocmd!
    autocmd ColorScheme * call ZenkakuSpace()
    autocmd VimEnter,WinEnter,BufRead * let w:m1=matchadd('ZenkakuSpace','　')
  augroup END
  call ZenkakuSpace()
endif
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" filitype
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" set filetypes as typescriptreact
autocmd BufNewFile,BufRead *.tsx,*.jsx set filetype=typescriptreact
autocmd BufNewFile,BufRead *.module.css set filetype=scss
autocmd FileType scss setl iskeyword+=@-@
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" lightline
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set laststatus=2
set t_Co=256

let g:lightline= {
  \ 'colorscheme': 'solarized'
  \ }


let g:lightline = {
  \ 'colorscheme': 'solarized',
  \ 'mode_map': {'c': 'NORMAL'},
  \ 'active': {
  \   'left': [
  \     ['mode', 'paste'],
  \     ['fugitive', 'gitgutter', 'filename'],
  \   ],
  \   'right': [
  \     ['cocstatus'],
  \     ['lineinfo'],
  \     ['percent'],
  \     ['charcode', 'fileformat', 'fileencoding', 'filetype'],
  \   ]
  \ },
  \ 'component_function': {
  \   'cocstatus': 'coc#status',
  \   'modified': 'MyModified',
  \   'readonly': 'MyReadonly',
  \   'fugitive': 'MyFugitive',
  \   'filename': 'MyFilename',
  \   'gitgutter': 'MyGitGutter',
  \ },
  \ }

function! MyModified()
  return &ft =~ 'help\|nerdtree' ? '' : &modified ? '+' : &modifiable ? '' : '-'
endfunction

function! MyReadonly()
  return &ft !~? 'help\|nerdtree' && &ro ? '⭤' : ''
endfunction

function! MyFilename()
  return ('' != MyReadonly() ? MyReadonly() . ' ' : '') .
        \ (&ft =~ 'denite' ? denite#get_status('sources') :
        \ '' != expand('%:t') ? expand('%:t') : '[No Name]') .
        \ ('' != MyModified() ? ' ' . MyModified() : '')
endfunction

function! MyFugitive()
  try
    if exists('*fugitive#head')
      let _ = fugitive#head()
      return strlen(_) ? "\u2d84  " ._ : ''
    endif
  catch
  endtry
  return ''
endfunction

augroup CocStatusRefresh
    autocmd!
    autocmd User CocStatusChange,CocDiagnosticChange call lightline#update()
augroup END

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Denite.nvim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Load key mappings for buffers of denite
augroup my_denite
    autocmd!
    autocmd FileType denite call s:denite_my_settings()
    autocmd FileType denite-filter call s:denite_filter_my_settings()
augroup END

" Set action map in denite buffer
function! s:denite_my_settings() abort
    nnoremap <silent><buffer><expr> <CR>
                \ denite#do_map('do_action')
    nnoremap <silent><buffer><expr> s
                \ denite#do_map('do_action', 'vsplit')
    nnoremap <silent><buffer><expr> o
                \ denite#do_map('do_action', 'split')
    nnoremap <silent><buffer><expr> d
                \ denite#do_map('do_action', 'delete')
    nnoremap <silent><buffer><expr> p
                \ denite#do_map('do_action', 'preview')
    nnoremap <silent><buffer><expr> q
                \ denite#do_map('quit')
    nnoremap <silent><buffer><expr> i
                \ denite#do_map('open_filter_buffer')
    nnoremap <silent><buffer><expr> <Space>
                \ denite#do_map('toggle_select').'j'
endfunction

" Set action map in denite-filter buffer
function! s:denite_filter_my_settings() abort
    imap <silent><buffer> <Esc> <Plug>(denite_filter_quit)
    imap <silent><buffer> <C-[> <Plug>(denite_filter_quit)
    inoremap <silent><buffer> <C-n> <Esc>
                \:call denite#move_to_parent()<CR>
                \:call cursor(line('.')+1,0)<CR>
                \:call denite#move_to_filter()<CR>A
    inoremap <silent><buffer> <C-p> <Esc>
                \:call denite#move_to_parent()<CR>
                \:call cursor(line('.')-1,0)<CR>
                \:call denite#move_to_filter()<CR>A
endfunction

" Define default options
call denite#custom#option('default', {
            \   'start-filter': v:true,
            \   'highlight_matched_char': 'None',
            \   'highlight_matched_range': 'Search',
            \   'direction': "top",
            \   'vertical_preview': v:true,
            \   'preview_width': float2nr(&columns / 2),
            \   'filter_split_direction': "top",
            \   'prompt': '> ',
            \   'smartcase': v:true,
            \   'start_filter': v:true,
            \ })

nnoremap <silent> <leader>b :<C-u>Denite buffer<CR>
nnoremap <silent> <leader>r :<C-u>Denite register<CR>
nnoremap <silent> <leader>m :<C-u>Denite mark<CR>
nnoremap <silent> <leader>p :<C-u>Denite file/rec<CR>
nnoremap <silent> <leader>f :<C-u>DeniteBufferDir file file:new<CR>
nnoremap <silent> <leader>/ :<C-u>DeniteProjectDir grep<CR>
nnoremap <silent> <leader>u :<C-u>Denite -resume -refresh<CR>

" Set custom searcher
if executable('rg')
    call denite#custom#var('file/rec', 'command',
                \ ['rg', '--files', '--hidden', '--glob', '!.git', '--color', 'never'])
    call denite#custom#var('grep', {
                \ 'command': ['rg'],
                \ 'default_opts': ['-S', '--vimgrep', '--no-heading', '--hidden', '--glob', '!.git'],
                \ 'recursive_opts': [],
                \ 'pattern_opt': ['--regexp'],
                \ 'separator': ['--'],
                \ 'final_opts': [],
                \ })
elseif executable('ag')
    call denite#custom#var('file/rec', 'command',
                \ ['ag', '--follow', '--nocolor', '--nogroup', '-g', ''])
    call denite#custom#var('grep', {
                \ 'command': ['ag'],
                \ 'default_opts': ['-i', '--vimgrep'],
                \ 'recursive_opts': [],
                \ 'pattern_opt': [],
                \ 'separator': ['--'],
                \ 'final_opts': [],
                \ })
endif

if &rtp =~ "devicons"
    call denite#custom#source('file', 'converters', ['devicons_denite_converter', 'converter/abbr_word'])
    call denite#custom#source('file/rec', 'converters', ['devicons_denite_converter', 'converter/abbr_word'])
    call denite#custom#source('grep', 'converters', ['devicons_denite_converter', 'converter/abbr_word'])
else
    call denite#custom#source('file', 'converters', ['converter/abbr_word'])
    call denite#custom#source('file/rec', 'converters', ['converter/abbr_word'])
    call denite#custom#source('grep', 'converters', ['converter/abbr_word'])
endif
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let NERDTreeShowHidden = 1
nnoremap <silent> <leader>t :NERDTreeToggle<CR>
command! -nargs=0 NT :NERDTreeToggle
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" git-gutter
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set signcolumn=yes
highlight clear SignColumn
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" coc-nvim
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Use tab for trigger completion with characters ahead and navigate.
" NOTE: Use command ':verbose imap <tab>' to make sure tab is not mapped by
" other plugin before putting this into your config.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use `[g` and `]g` to navigate diagnostics
" Use `:CocDiagnostics` to get all diagnostics of current buffer in location list.
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K to show documentation in preview window.
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  elseif (coc#rpc#ready())
    call CocActionAsync('doHover')
  else
    execute '!' . &keywordprg . " " . expand('<cword>')
  endif
endfunction

" Symbol renaming.
nmap <leader>rn <Plug>(coc-rename)

" yank list setting
nnoremap <silent> <leader>y :<C-u>CocList -A --normal yank<cr>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Tagbar, ctags
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nnoremap <silent><C-j> :TagbarToggle<CR>
nnoremap <C-]> g<C-]>
