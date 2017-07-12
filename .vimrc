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
NeoBundle 'scrooloose/nerdcommenter'
NeoBundle 'Townk/vim-autoclose'
NeoBundle 'junegunn/vim-easy-align'
NeoBundle 'itchyny/lightline.vim'
NeoBundle 'mattn/emmet-vim'
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
"plugin関係なし
""""""""""""""""""""""
set autoindent
set expandtab
set smartindent
set shiftwidth=2
set ruler
set number
set title
set ambiwidth=double
set tabstop=4
set list
set listchars=tab:»-,trail:-,eol:↲,extends:»,precedes:«,nbsp:%
set nrformats-=octal
set hidden
set history=50
set virtualedit=block
set whichwrap=b,s,[,],<,>
set backspace=indent,eol,start
set wildmenu
syntax on

"""""""""""""""""""""
"colorscheme
"""""""""""""""""""""
colorscheme solarized

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
" 挿入モード時にステータス行の色を変える
""""""""""""""""""""""""""""""
let g:hi_insert='highlight StatusLine guifg=darkblue guibg=darkyellow gui=none ctermfg=blue ctermbg=yellow cterm=none'
if has('syntax')
    augroup InsetHook
        autocmd!
        autocmd InsertEnter * call s:StatusLine('Enter')
        autocmd InsertLeave * call s:StatusLine('Leave')
    augroup END
endif

let s:slhlcmd=''
function! s:StatusLine(mode)
    if a:mode=='Enter'
        silent! let s:slhlcmd='highlight ' . s:GetHighlight('StatusLine')
        silent exec g:hi_insert
    else
        highlight clear StatusLine
        silent exec s:slhlcmd
    endif
endfunction

function! s:GetHighlight(hi)
    redir => hl
    exec 'highlight '.a:hi
    let hl = substitute(hl,'[\r\n]','','g')
    let hl = substitute(hl,'xxx','','')
    return hl
endfunction
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" paste時のインデントの崩れを防ぐ
""""""""""""""""""""""""""""""
set pastetoggle=<F10>
nnoremap <F10> :set paste!<CR>:set paste?<CR>
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" カーソル位置の復元
""""""""""""""""""""""""""""""
if has('autocmd')
    autocmd BufReadPost * if line("'\"") > 0 && line ("'\"") <= line("$") | exe "normal! g'\"" | endif
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
nnoremap <silent><C-e> :NERDTreeToggle<CR>


