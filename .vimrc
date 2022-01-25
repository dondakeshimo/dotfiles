"""""""""""""""""""""""
" init
"""""""""""""""""""""""
" viとの互換性を一応切る
if &compatible
  set nocompatible
endif

set encoding=UTF-8

filetype plugin indent on
""""""""""""""""""""""

""""""""""""""""""""""
" plugin関係なし
""""""""""""""""""""""
" vimの見た目系
set ruler
set number
set title
set ambiwidth=double
set list
set listchars=tab:»-,trail:-,extends:»,precedes:«,nbsp:%
" 空白系
set autoindent
set smartindent
set shiftwidth=4
set expandtab
set tabstop=4
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
set clipboard=unnamed
" updatetime
set updatetime=100
""""""""""""""""""""""

"""""""""""""""""""""
" colorscheme
"""""""""""""""""""""
syntax enable
"""""""""""""""""""""

"""""""""""""""""""""
" insertモードでのキーマップ
"""""""""""""""""""""
inoremap <C-b> <Left>
inoremap <C-f> <Right>
inoremap <C-a> <C-o>^
inoremap <C-e> <C-o>$
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
