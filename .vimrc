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
NeoBundle 'Shougo/neosnippet.vim'
NeoBundle 'ujihisa/unite-colorscheme'

NeoBundle 'altercation/vim-colors-solarized'
NeoBundle 'tomasr/molokai'
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
" カーソル位置の復元
""""""""""""""""""""""""""""""
if has('autocmd')
    autocmd BufReadPost * if line("'\"") > 0 && line ("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
