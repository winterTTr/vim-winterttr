let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
imap <F12> <F12>
imap <silent> <Plug>IMAP_JumpBack =IMAP_Jumpfunc('b', 0)
imap <silent> <Plug>IMAP_JumpForward =IMAP_Jumpfunc('', 0)
inoremap <silent> <BS> =TTrCodeAssistor_IntelligentBackspace()
inoremap <silent> <S-Tab> =TTrCodeAssistor_Action("b")
inoremap <silent> <C-CR> =TTrCodeAssistor_ExpandTemplates()
inoremap <F4> :q
map! <S-Insert> *
snoremap <silent> 	 <Left>a=TTrCodeAssistor_Action("")
vmap <NL> <Plug>IMAP_JumpForward
nmap <NL> <Plug>IMAP_JumpForward
nnoremap  
nnoremap  :call TTr_ToggleFold()
nnoremap  p
vnoremap <silent>  :if expand("%") == "" |browse confirm update |else |confirm update |endif
nnoremap <silent>  :if expand("%") == "" |browse confirm update |else |confirm update |endif
vmap  "*d
map  a
nnoremap   }
noremap ,e :e =expand("%:p:h")."\\"
xnoremap < <gv
xnoremap > >gv
inoremap ë gT
inoremap ê gt
cnoremap é =substitute(getline('.')[(col('.')-1):],'\W.*','','g')
cnoremap î /=histget('/',-1)
nmap \cv <Plug>VCSVimDiff
nmap \cu <Plug>VCSUpdate
nmap \cU <Plug>VCSUnlock
nmap \cs <Plug>VCSStatus
nmap \cr <Plug>VCSReview
nmap \cq <Plug>VCSRevert
nmap \cl <Plug>VCSLog
nmap \cL <Plug>VCSLock
nmap \ci <Plug>VCSInfo
nmap \cg <Plug>VCSGotoOriginal
nmap \cd <Plug>VCSDiff
nmap \cD <Plug>VCSDelete
nmap \cc <Plug>VCSCommit
nmap \cG <Plug>VCSClearAndGotoOriginal
nmap \cn <Plug>VCSAnnotate
nmap \ca <Plug>VCSAdd
nmap <silent> \n <Plug>MarkClear
vmap <silent> \r <Plug>MarkRegex
nmap <silent> \r <Plug>MarkRegex
vmap <silent> \m <Plug>MarkSet
nmap <silent> \m <Plug>MarkSet
nmap \caL <Plug>CalendarH
nmap \cal <Plug>CalendarV
map <silent> \bv :VSBufExplorer
map <silent> \bs :SBufExplorer
map <silent> \be :BufExplorer
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
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#NetBrowseX(expand("<cWORD>"),0)
nnoremap <silent> <Plug>CVSWatchRemove :CVSWatch remove
nnoremap <silent> <Plug>CVSWatchOn :CVSWatch on
nnoremap <silent> <Plug>CVSWatchOff :CVSWatch off
nnoremap <silent> <Plug>CVSWatchAdd :CVSWatch add
nnoremap <silent> <Plug>CVSWatchers :CVSWatchers
nnoremap <silent> <Plug>CVSUnedit :CVSUnedit
nnoremap <silent> <Plug>CVSEditors :CVSEditors
nnoremap <silent> <Plug>CVSEdit :CVSEdit
nnoremap <silent> <Plug>VCSVimDiff :VCSVimDiff
nnoremap <silent> <Plug>VCSUpdate :VCSUpdate
nnoremap <silent> <Plug>VCSUnlock :VCSUnlock
nnoremap <silent> <Plug>VCSStatus :VCSStatus
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
vmap <silent> <Plug>IMAP_JumpBack `<i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpBack "_<Del>i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpForward "_<Del>i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>IMAP_JumpBack i=IMAP_Jumpfunc('b', 0)
nmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>CalendarH :cal Calendar(1)
nmap <silent> <Plug>CalendarV :cal Calendar(0)
snoremap <silent> <S-Tab> <Left>F`i=TTrCodeAssistor_Action("b")
nmap <F5> :py RunCurrentFile()
nmap <S-F12> :py RunDebugger()
nmap <S-F7> :py RemoveBreakpoints()
vnoremap <F7> :call TTrCodeAssistor_ToggleComments()
nmap <F7> :py SetBreakpoint()
nnoremap <silent> <F8> :TlistToggle
nnoremap <silent> <C-F6> :!start cmd.exe
nnoremap <silent> <C-F5> :if expand("%:p:h") != "" |execute '!start explorer.exe '.substitute(expand("%:p:h"),'/','\','g')|endif
nmap <F11> :set guifont=*
nmap <F10> :set guifont=GB_YuanHei:h12:cGB2312
nmap <F9> :set guifont=Lucida_Sans_Typewriter:h11:cANSI
vnoremap <F4> :q
nnoremap <F4> :q
noremap <Down> gj
noremap <Up> gk
vmap <C-Del> "*d
vmap <S-Del> "*d
vmap <C-Insert> "*y
vmap <S-Insert> "-d"*P
nmap <S-Insert> "*P
inoremap  <Left>
cnoremap  <Left>
inoremap <silent> 	 =TTrCodeAssistor_Action("")
imap <NL> <Plug>IMAP_JumpForward
cnoremap <NL> <Down>
inoremap  <Up>
cnoremap  <Up>
inoremap  <Right>
cnoremap  <Right>
inoremap <silent>  :if expand("%") == "" |browse confirm update |else |confirm update |endif
inoremap <expr>  omni#cpp#maycomplete#Complete()
inoremap  =GetCloseTag()
inoremap <silent> ( =TTrCodeAssistor_CompleteFuncPrototypeFromTags()
inoremap <silent> ) =TTrCodeAssistor_IntelligentRightBracket()
inoremap <expr> . omni#cpp#maycomplete#Dot()
inoremap <expr> : omni#cpp#maycomplete#Scope()
inoremap <expr> > omni#cpp#maycomplete#Arrow()
nnoremap ® :call search ("^". matchstr (getline (line (".")), '\(\s*\)') ."\\S")^
nnoremap ¬ k:call search ("^". matchstr (getline (line (".")+ 1), '\(\s*\)') ."\\S", 'b')^
nnoremap <silent> ¯ :nohl
nnoremap <silent> ï :call SwitchBetweenProgrammingFile()
nnoremap ë gT
nnoremap ê gt
noremap Ý :tab split
let &cpo=s:cpo_save
unlet s:cpo_save
set autoindent
set autoread
set background=dark
set backspace=eol,indent,start
set clipboard=autoselect
set confirm
set cscopequickfix=c-,d-,e-,f-,g-,i-,s-,t-
set cscopetag
set cscopeverbose
set diffopt=filler,context:3,vertical
set display=lastline,uhex
set encoding=utf-8
set expandtab
set fileencodings=ucs-bom,utf-8,cp932,cp936,cp950,prc,latin1
set formatoptions=tcql
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
set omnifunc=omni#cpp#complete#Main
set ruler
set selectmode=key
set shellslash
set shiftwidth=4
set showmatch
set smartcase
set smartindent
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
cd D:\NvPRO_IT_ENV\target\src\cmd\NvPROFlowCollector\NvPROFlowCollectorSvc
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 resource.h
badd +1 
badd +1 NvPROFlowCollectorChildWnd.cpp
badd +133 E:/Tools/Vim/_vimrc
args resource.h
edit resource.h
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal noarabic
setlocal autoindent
setlocal autoread
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal cindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal comments=sr:/*,mb:*,ex:*/,://
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
setlocal expandtab
if &filetype != 'cpp'
setlocal filetype=cpp
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
setlocal formatoptions=croql
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
setlocal keymap=
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
setlocal omnifunc=omni#cpp#complete#Main
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
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=
setlocal noswapfile
setlocal synmaxcol=3000
if &syntax != 'cpp'
setlocal syntax=cpp
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=72
setlocal thesaurus=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 1 - ((0 * winheight(0) + 21) / 43)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
tabedit NvPROFlowCollectorChildWnd.cpp
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal noarabic
setlocal autoindent
setlocal autoread
setlocal balloonexpr=
setlocal nobinary
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal cindent
setlocal cinkeys=0{,0},0),:,0#,!^F,o,O,e
setlocal cinoptions=
setlocal cinwords=if,else,while,do,for,switch
setlocal comments=sr:/*,mb:*,ex:*/,://
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
setlocal expandtab
if &filetype != 'cpp'
setlocal filetype=cpp
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
setlocal formatoptions=croql
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
setlocal keymap=
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
setlocal omnifunc=omni#cpp#complete#Main
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
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=
setlocal noswapfile
setlocal synmaxcol=3000
if &syntax != 'cpp'
setlocal syntax=cpp
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=72
setlocal thesaurus=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 1 - ((0 * winheight(0) + 21) / 43)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
tabnext 2
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
