"""""""""""""""""""""""
" dein.vim
"""""""""""""""""""""""
if &compatible
  set nocompatible
endif

let s:dein_dir = expand('~/.vim/bundles')
let s:dein_repo_dir = expand('~/Scripts/src/github.com/Shougo/dein.vim')

if &runtimepath !~# '/dein.vim'
  if !isdirectory(s:dein_repo_dir)
    execute '!ghq get https://github.com/Shougo/dein.vim' s:dein_repo_dir
  endif
  execute 'set runtimepath^=' . fnamemodify(s:dein_repo_dir, ':p')
endif

if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)

  call dein#add(s:dein_dir)
  call dein#add('Shougo/deoplete.nvim')
  call dein#add('Shougo/unite.vim')
  call dein#add('Shougo/neomru.vim')
  call dein#add('Townk/vim-autoclose')
  call dein#add('itchyny/lightline.vim')
  call dein#add('Yggdroot/indentLine')
  call dein#add('Shougo/vimproc.vim', {'build' : 'make'})

  call dein#add('altercation/vim-colors-solarized')
  call dein#add('ujihisa/unite-colorscheme')

  call dein#end()
  call dein#save_state()
endif

filetype plugin indent on
""""""""""""""""""""""

""""""""""""""""""""""
" plugin関係なし
""""""""""""""""""""""
" vimの見た目系
set ruler
set number
set title
" 空白系
set autoindent
set smartindent
set shiftwidth=4
set expandtab
set tabstop=4
set ambiwidth=double
set list
set listchars=tab:»-,trail:-,eol:↲,extends:»,precedes:«,nbsp:%
" カーソル系
set whichwrap=b,s,[,],<,>
set backspace=indent,eol,start
set virtualedit=block
set ttimeoutlen=10
" ファイル操作系
set noswapfile
set hidden
set wildmenu
set backupdir=$HOME/.vimbackup
" 文字列系
set nrformats-=octal
" 検索系
set ignorecase
set smartcase
set hlsearch
set incsearch
set wrapscan
" クリップボードにコピー
set clipboard=unnamed,autoselect
""""""""""""""""""""""

"""""""""""""""""""""
"colorscheme
"""""""""""""""""""""
set background=dark
colorscheme solarized
syntax enable
"""""""""""""""""""""

""""""""""""""""""""""""""""""
" 全角スペースの可視化
""""""""""""""""""""""""""""""
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
""""""""""""""""""""""""""""""


""""""""""""""""""""""""""""""
"lightline
""""""""""""""""""""""""""""""
set laststatus=2
set t_Co=256
let g:lightline = {
  \ 'colorscheme': 'solarized'
  \ }
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" Unit.vim
""""""""""""""""""""""""""""""
" 入力モードで開始する
let g:unite_enable_start_insert=1
let g:unite_source_file_mru_limit = 200
nnoremap <silent> ,ub :<C-u>Unite buffer<CR>
nnoremap <silent> ,uf :<C-u>UniteWithBufferDir -buffer-name=files file<CR>
nnoremap <silent> ,uu :<C-u>Unite file_mru buffer<CR>
""""""""""""""""""""""""""""""
