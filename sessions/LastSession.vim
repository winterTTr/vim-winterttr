let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
map! <S-Insert> *
vnoremap <silent>  :q
nnoremap <silent>  :q
nnoremap <NL> 
nnoremap  
nnoremap  :call TTr_ToggleFold()
nnoremap  p
vmap  "*d
nnoremap   }
nnoremap ,e :e =expand("%:p:h")."\\"
xnoremap < <gv
xnoremap > >gv
cnoremap ì 
cnoremap é =substitute(getline('.')[(col('.')-1):],'\W.*','','g')
cnoremap î /=histget('/',-1)
nmap <silent> \cv <Plug>VCSVimDiff
nmap <silent> \cu <Plug>VCSUpdate
nmap <silent> \cU <Plug>VCSUnlock
nmap <silent> \cs <Plug>VCSStatus
nmap <silent> \cr <Plug>VCSReview
nmap <silent> \cq <Plug>VCSRevert
nmap <silent> \cn <Plug>VCSAnnotate
nmap <silent> \cN <Plug>VCSSplitAnnotate
nmap <silent> \cl <Plug>VCSLog
nmap <silent> \cL <Plug>VCSLock
nmap <silent> \ci <Plug>VCSInfo
nmap <silent> \cg <Plug>VCSGotoOriginal
nmap <silent> \cG <Plug>VCSClearAndGotoOriginal
nmap <silent> \cd <Plug>VCSDiff
nmap <silent> \cD <Plug>VCSDelete
nmap <silent> \cc <Plug>VCSCommit
nmap <silent> \ca <Plug>VCSAdd
nnoremap <silent> \z :set foldexpr=getline(v:lnum)!~@/ foldlevel=0 foldcolumn=0 foldmethod=expr
nmap gx <Plug>NetrwBrowseX
nmap gnd :cs find d =expand("<cword>")
nmap gni :cs find i ^=expand("<cfile>")$
nmap gnf :cs find f =expand("<cfile>")
nmap gne :cs find e =expand("<cword>")
nmap gnt :cs find t =expand("<cword>")
nmap gnc :cs find c =expand("<cword>")
nmap gng :cs find g =expand("<cword>")
nmap gns :cs find s =expand("<cword>")
nnoremap p pmz=`]`z
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#NetrwBrowseX(expand("<cWORD>"),0)
nnoremap <silent> <Plug>VCSVimDiff :VCSVimDiff
nnoremap <silent> <Plug>VCSUpdate :VCSUpdate
nnoremap <silent> <Plug>VCSUnlock :VCSUnlock
nnoremap <silent> <Plug>VCSStatus :VCSStatus
nnoremap <silent> <Plug>VCSSplitAnnotate :VCSAnnotate!
nnoremap <silent> <Plug>VCSReview :VCSReview
nnoremap <silent> <Plug>VCSRevert :VCSRevert
nnoremap <silent> <Plug>VCSLog :VCSLog
nnoremap <silent> <Plug>VCSLock :VCSLock
nnoremap <silent> <Plug>VCSInfo :VCSInfo
nnoremap <silent> <Plug>VCSClearAndGotoOriginal :VCSGotoOriginal!
nnoremap <silent> <Plug>VCSGotoOriginal :VCSGotoOriginal
nnoremap <silent> <Plug>VCSDiff :VCSDiff
nnoremap <silent> <Plug>VCSDelete :VCSDelete
nnoremap <silent> <Plug>VCSCommit :VCSCommit
nnoremap <silent> <Plug>VCSAnnotate :VCSAnnotate
nnoremap <silent> <Plug>VCSAdd :VCSAdd
nnoremap <silent> <F8> :TlistToggle
nnoremap <silent> <C-F6> :execute '!start cmd.exe /k cd /d "' . expand("%:h") . '"'
nnoremap <silent> <C-F5> :if expand("%:p:h") != "" |execute '!start explorer /e,/select,'.substitute(expand("%:p"),'/','\','g')|endif
noremap <Down> gj
noremap <Up> gk
vmap <C-Del> "*d
vmap <S-Del> "*d
vmap <C-Insert> "*y
vmap <S-Insert> "-d"*P
nmap <S-Insert> "*P
inoremap <silent>  :q
inoremap  <Left>
cnoremap  <Left>
inoremap 	 =g:Coder_MagicKey("Tab")
inoremap <NL> <Down>
cnoremap <NL> <Down>
inoremap  <Up>
cnoremap  <Up>
inoremap  <Right>
cnoremap  <Right>
inoremap ( =g:Coder_MagicKey("(")
inoremap ) =g:Coder_MagicKey(")")
nnoremap ® :call search ("^". matchstr (getline (line (".")), '\(\s*\)') ."\\S")^
nnoremap ¬ k:call search ("^". matchstr (getline (line (".")+ 1), '\(\s*\)') ."\\S", 'b')^
nnoremap <silent> ¯ :nohl
nnoremap <silent> ï :call SwitchBetweenProgrammingFile()
noremap Ý :tab split
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set autoread
set background=dark
set backspace=eol,indent,start
set balloonexpr=GetTagSignature()
set clipboard=autoselect
set confirm
set cscopequickfix=c-,d-,e-,f-,g-,i-,s-,t-
set cscopetag
set cscopeverbose
set diffopt=filler,context:6,vertical
set display=lastline,uhex
set encoding=utf-8
set fileencodings=ucs-bom,utf-8,cp932,cp936,cp950,prc,latin1
set grepprg=grep\ -nH\ $*
set guifont=Bitstream_Vera_Sans_Mono:h11:cANSI
set guifontwide=NSimsun:h12
set guioptions=aegimtrL
set helplang=cn
set history=100
set hlsearch
set ignorecase
set iminsert=1
set imsearch=1
set incsearch
set infercase
set keymodel=startsel,stopsel
set langmenu=none
set laststatus=2
set ruler
set selectmode=key
set shellslash
set shiftwidth=4
set showmatch
set smartcase
set statusline=%<%f%m\ [%{&ff}:%{&fenc}:%Y]\ %{getcwd()}\ \ [%{strftime('%Y/%b/%d\ %a\ %I:%M\ %p')}]\ %=\ Line:%l/%L\ Column:%c%V\ %P
set noswapfile
set switchbuf=useopen,usetab
set tabstop=4
set textwidth=72
set title
set wildmenu
set wildmode=longest,list
set window=44
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd D:\Tools\VIM_72\bin
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
silent! argdel *
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
enew
setlocal keymap=
setlocal noarabic
setlocal autoindent
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal comments=s1:/*,mb:*,ex:*/,://,b:#,:%,:XCOMM,n:>,fb:-
setlocal commentstring=/*%s*/
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal nocopyindent
setlocal nocursorcolumn
setlocal nocursorline
setlocal define=
setlocal dictionary=
setlocal nodiff
setlocal equalprg=
setlocal errorformat=
setlocal noexpandtab
if &filetype != ''
setlocal filetype=
endif
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=0
setlocal foldmarker={{{,}}}
set foldmethod=marker
setlocal foldmethod=marker
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatoptions=tcq
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
setlocal grepprg=
setlocal iminsert=1
setlocal imsearch=1
setlocal include=
setlocal includeexpr=
setlocal indentexpr=
setlocal indentkeys=0{,0},:,0#,!^F,o,O,e
setlocal infercase
setlocal iskeyword=@,48-57,_,128-167,224-235
setlocal keywordprg=
set linebreak
setlocal linebreak
setlocal nolisp
setlocal nolist
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=octal,hex
set number
setlocal number
setlocal numberwidth=4
setlocal omnifunc=
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal shiftwidth=4
setlocal noshortname
setlocal nosmartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=
setlocal noswapfile
setlocal synmaxcol=3000
if &syntax != ''
setlocal syntax=
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=72
setlocal thesaurus=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . s:sx
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
