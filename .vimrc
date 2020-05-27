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
  call dein#add('ryanoasis/vim-devicons')
  call dein#add('dense-analysis/ale')
  call dein#add('tpope/vim-fugitive')
  call dein#add('tpope/vim-surround')
  call dein#add('airblade/vim-gitgutter')
  call dein#add('majutsushi/tagbar')
  call dein#add('davidhalter/jedi-vim', {'on_ft' : ['python']})
  call dein#add('itchyny/lightline.vim')
  call dein#add('maximbaz/lightline-ale')
  call dein#add('Yggdroot/indentLine')
  call dein#add('Shougo/vimproc.vim', {'build' : 'make'})
  call dein#add('altercation/vim-colors-solarized')
  call dein#add('ujihisa/unite-colorscheme')

  " nerd-fontのインストール必須
  call dein#add('Xuyuanp/nerdtree-git-plugin')

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
" updatetime
set updatetime=100
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
      return strlen(_) ? "\u2d84  " ._ : ''
    endif
  catch
  endtry
  return ''
endfunction

let g:lightline#ale#indicator_checking = "\u21ba"
let g:lightline#ale#indicator_infos = "\u2139"
let g:lightline#ale#indicator_warnings = "\u26a0"
let g:lightline#ale#indicator_errors = "\u2620"
let g:lightline#ale#indicator_ok = "\u2714"

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

" mruファイルの上限設定
let g:unite_source_file_mru_limit = 200

" " 大文字小文字を区別しない
let g:unite_enable_ignore_case = 1
let g:unite_enable_smart_case = 1

" キーマップ設定
nnoremap <silent> ,ub :<C-u>Unite buffer<CR>
nnoremap <silent> ,uf :<C-u>UniteWithBufferDir -buffer-name=files file<CR>
nnoremap <silent> ,uu :<C-u>Unite file_mru buffer<CR>

" grep検索
nnoremap <silent> ,g  :<C-u>Unite grep:. -buffer-name=search-buffer<CR>
" ディレクトリを指定してgrep検索
nnoremap <silent> ,dg  :<C-u>Unite grep -buffer-name=search-buffer<CR>
" grep検索結果の再呼出
nnoremap <silent> ,r  :<C-u>UniteResume search-buffer<CR>

" unite grep に ag(The Silver Searcher) を使う
if executable('ag')
  let g:unite_source_grep_command = 'ag'
  let g:unite_source_grep_default_opts = '--nogroup --nocolor --column'
  let g:unite_source_grep_recursive_opt = ''
endif

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
let g:ale_sign_error = "\u2620"
let g:ale_sign_warning = "\u26a0"
""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""
" Tagbar, ctags
""""""""""""""""""""""""""""""
nnoremap <silent><C-j> :TagbarToggle<CR>
nnoremap <C-]> g<C-]>
