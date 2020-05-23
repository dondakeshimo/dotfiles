"""""""""""""""""""""""
" init
"""""""""""""""""""""""
" viとの互換性を一応切る
if &compatible
  set nocompatible
endif

set encoding=UTF-8


"""""""""""""""""""""""
" dein.vim
"""""""""""""""""""""""
" dein.vimのrepositoryを設定
let s:dein_dir = expand('~/.vim/bundles')
let s:dein_repo_dir = expand('~/Scripts/src/github.com/Shougo/dein.vim')

" dein.vimがなければinstall
if &runtimepath !~# '/dein.vim'
  if !isdirectory(s:dein_repo_dir)
    execute '!ghq get https://github.com/Shougo/dein.vim' s:dein_repo_dir
  endif
  execute 'set runtimepath^=' . fnamemodify(s:dein_repo_dir, ':p')
endif

" dein.vimのセットアップ
if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)
  call dein#add(s:dein_dir)

  call dein#add('Shougo/unite.vim')
  call dein#add('Shougo/neomru.vim')
  call dein#add('preservim/nerdtree')
  call dein#add('Xuyuanp/nerdtree-git-plugin')
  call dein#add('ryanoasis/vim-devicons')
  call dein#add('dense-analysis/ale')
  call dein#add('tpope/vim-fugitive')
  call dein#add('tpope/vim-surround')
  call dein#add('airblade/vim-gitgutter')
  call dein#add('majutsushi/tagbar')
  call dein#add('davidhalter/jedi-vim')
  call dein#add('itchyny/lightline.vim')
  call dein#add('maximbaz/lightline-ale')
  call dein#add('Yggdroot/indentLine')
  call dein#add('Shougo/vimproc.vim', {'build' : 'make'})
  call dein#add('altercation/vim-colors-solarized')
  call dein#add('ujihisa/unite-colorscheme')

  call dein#end()
  call dein#save_state()
endif

" 自動インストール
if has('vim_starting') && dein#check_install()
  call dein#install()
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
set colorcolumn=80
" 空白系
set autoindent
set smartindent
set shiftwidth=4
set expandtab
set tabstop=4
set ambiwidth=double
set list
set listchars=tab:»-,trail:-,extends:»,precedes:«,nbsp:%
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
" colorscheme
"""""""""""""""""""""
set background=dark
colorscheme solarized
syntax enable
"""""""""""""""""""""

"""""""""""""""""""""
" insertモードでのキーマップ
"""""""""""""""""""""
noremap! <C-b> <Left>
noremap! <C-f> <Right>
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

""""""""""""""""""""""""""""""
" lightline
""""""""""""""""""""""""""""""
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
  \     ['linter_checking', 'linter_errors', 'linter_warnings', 'linter_infos', 'linter_ok'],
  \     ['percent'],
  \     ['charcode', 'fileformat', 'fileencoding', 'filetype'],
  \   ]
  \ },
  \ 'component_function': {
  \   'modified': 'MyModified',
  \   'readonly': 'MyReadonly',
  \   'fugitive': 'MyFugitive',
  \   'filename': 'MyFilename',
  \   'gitgutter': 'MyGitGutter',
  \ },
  \ 'separator': {'left': '⮀', 'right': '⮂'},
  \ 'subseparator': {'left': '⮁', 'right': '⮃'}
  \ }

function! MyModified()
  return &ft =~ 'help\|nerdtree' ? '' : &modified ? '+' : &modifiable ? '' : '-'
endfunction

function! MyReadonly()
  return &ft !~? 'help\|nerdtree' && &ro ? '⭤' : ''
endfunction

function! MyFilename()
  return ('' != MyReadonly() ? MyReadonly() . ' ' : '') .
        \ (&ft == 'unite' ? unite#get_status_string() :
        \ '' != expand('%:t') ? expand('%:t') : '[No Name]') .
        \ ('' != MyModified() ? ' ' . MyModified() : '')
endfunction

function! MyFugitive()
  try
    if exists('*fugitive#head')
      let _ = fugitive#head()
      return strlen(_) ? '⭠ '._ : ''
    endif
  catch
  endtry
  return ''
endfunction

let g:lightline#ale#indicator_checking = "\uf110"
let g:lightline#ale#indicator_infos = "\uf129"
let g:lightline#ale#indicator_warnings = "\uf071"
let g:lightline#ale#indicator_errors = "\uf05e"
let g:lightline#ale#indicator_ok = "\uf00c"

let g:lightline.component_expand = {
 \ 'linter_checking': 'lightline#ale#checking',
 \ 'linter_infos': 'lightline#ale#infos',
 \ 'linter_warnings': 'lightline#ale#warnings',
 \ 'linter_errors': 'lightline#ale#errors',
 \ 'linter_ok': 'lightline#ale#ok',
 \ }

let g:lightline.component_type = {
 \ 'linter_checking': 'right',
 \ 'linter_infos': 'right',
 \ 'linter_warnings': 'warning',
 \ 'linter_errors': 'error',
 \ 'linter_ok': 'right',
 \ }

""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" Unit.vim
""""""""""""""""""""""""""""""
" 入力モードで開始する
let g:unite_enable_start_insert = 1
let g:unite_source_file_mru_limit = 200
nnoremap <silent> ,ub :<C-u>Unite buffer<CR>
nnoremap <silent> ,uf :<C-u>UniteWithBufferDir -buffer-name=files file<CR>
nnoremap <silent> ,uu :<C-u>Unite file_mru buffer<CR>
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" NERDTree
""""""""""""""""""""""""""""""
nnoremap <silent><C-e> :NERDTreeToggle<CR>
let NERDTreeShowHidden = 1
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" git-gutter
""""""""""""""""""""""""""""""
set signcolumn=yes
highlight clear SignColumn
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" ale
""""""""""""""""""""""""""""""
let g:ale_sign_error = "\uf05e"
let g:ale_sign_warning = "\uf071"
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" Tagbar, ctags
""""""""""""""""""""""""""""""
nnoremap <silent><C-j> :TagbarToggle<CR>
nnoremap <C-]> g<C-]>
