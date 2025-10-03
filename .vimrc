set nocompatible

filetype off
filetype plugin on
filetype indent on

syntax on

" indent related
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set smarttab

" search related
set hlsearch
set ignorecase
set smartcase
set incsearch

" line number related
set relativenumber  " show current line number
set number

" other
set nowrap
set smoothscroll

set mouse+=a
set shortmess+=I

set backspace=indent,eol,start
set laststatus=2

nnoremap <Left>  :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up>    :echoe "Use k"<CR>
nnoremap <Down>  :echoe "Use j"<CR>

nnoremap <C-j> <C-e>
nnoremap <C-k> <C-y>
noremap H ^
noremap L $

" press enter to send a command from a vim file to a tmux window
" nnoremap <enter> :.w !xargs -0ri tmux send -t1 {}<CR>j

nnoremap <Leader>b :buffers<CR>:buffer<Space>

" local customizations in ~/.vimrc_local
" let $LOCALFILE=expand("~/.vimrc_local")
" if filereadable($LOCALFILE)
"     source $LOCALFILE
" endif

autocmd FileType python,sh,fish set commentstring=#\ %s
autocmd FileType c,cpp,java,scala,cuda set commentstring=//\ %s
autocmd FileType vim set commentstring=\"\ %s
autocmd FileType markdown set commentstring=<!--\ %s\ -->
autocmd FileType sql set commentstring=--\ %s
