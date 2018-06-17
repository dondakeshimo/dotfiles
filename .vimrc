set nocompatible
filetype plugin indent off

if has('vim_starting')
    set runtimepath+=~/.vim/bundle/neobundle.vim
endif

"""""""""""""""""""""""
" NeoBundle begin
"""""""""""""""""""""""
let g:neobundle_default_git_protocol='https'
call neobundle#begin(expand('~/.vim/bundle'))
NeoBundleFetch 'Shougo/neobundle.vim'

NeoBundle 'Shougo/unite.vim'
NeoBundle 'Shougo/neomru.vim'
NeoBundle 'Shougo/neocomplcache'
NeoBundle 'tpope/vim-surround'
NeoBundle 'tpope/vim-fugitive'
NeoBundle 'scrooloose/nerdtree'
NeoBundle 'Townk/vim-autoclose'
NeoBundle 'junegunn/vim-easy-align'
NeoBundle 'itchyny/lightline.vim'
NeoBundle 'mattn/emmet-vim'
NeoBundle 'Yggdroot/indentLine'
NeoBundle 'rking/ag.vim'
NeoBundle 'Shougo/vimproc', {
    \'build' : {
    \   'windows' : 'make -f make_ningw32.mak',
    \   'cygwin'  : 'make -f make_cygwin.mak',
    \   'mac'     : 'make -f make_mac.mak',
    \   'unix'    : 'make -f make_unix.mak',
    \ },
\ }

NeoBundle 'altercation/vim-colors-solarized'
NeoBundle 'tomasr/molokai'
NeoBundle 'ujihisa/unite-colorscheme'
call neobundle#end()
""""""""""""""""""""""
"NeoBundle end
""""""""""""""""""""""

filetype plugin indent on

""""""""""""""""""""""
" plugin関係なし
""""""""""""""""""""""
" vimの見た目系
set ruler
set number
set title
syntax on
" 空白系
set autoindent
set smartindent
set shiftwidth=2
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
"NeoBundle
"lightline
""""""""""""""""""""""""""""""
set laststatus=2
set t_Co=256
let g:lightline = {
    \ 'colorscheme': 'solarized'
    \ }
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" NeoBundle
" Unit.vimの設定
""""""""""""""""""""""""""""""
" 入力モードで開始する
let g:unite_enable_start_insert=1
" バッファ一覧
noremap <C-P> :Unite buffer<CR>
" ファイル一覧
noremap <C-N> :Unite -buffer-name=file file<CR>
" 最近使ったファイルの一覧
noremap <C-F> :Unite file_mru<CR>
" sourcesを「今開いているファイルのディレクトリ」とする
noremap :uff :<C-u>UniteWithBufferDir file -buffer-name=file<CR>
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" NeoBundle
" NERDTree
""""""""""""""""""""""""""""""
" Ctrl + eでNERDTreeを起動
nnoremap <silent><C-e> :NERDTreeToggle<CR>
""""""""""""""""""""""""""""""


""""""""""""""""""""""""""""""
" NeoBundle
" neocomplecache
""""""""""""""""""""""""""""""
" vim起動時にneocomplecacheを有効化
" let g:neocomplcache_enable_at_startup=1
" 大文字と小文字の区別を大文字が入力されるまで無視
" let g:neocomplcache_enable_smart_case=1
" '_' を区切りとしたワイルドカード検索
" let g:neocomplcache_enable_underbar_completion=1
" キャッシュの最小文字長を3にする
" let g:neocomplcache_min_syntax_length=3
" dictionaryの設定
" let g:neocomplcache_dictionary_filetype_lists = {
"     \ 'default' : ''
"     \ }

" Ctrl + gで前回行われた保管をキャンセル
" inoremap <expr><C-g>     neocomplcache#undo_completion()
" Ctrl + l で保管候補の中から共通する部分を保管(shell like)
" inoremap <expr><C-l>     neocomplcache#complete_common_string()
" TABで補完候補の選択
" inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" pop upを消す系
" inoremap <expr><C-h> neocomplcache#smart_close_popup()."\<C-h>"
" inoremap <expr><BS> neocomplcache#smart_close_popup()."\<C-h>"
" inoremap <expr><C-y>  neocomplcache#close_popup()
" inoremap <expr><C-v>  neocomplcache#cancel_popup()
""""""""""""""""""""""""""""""
