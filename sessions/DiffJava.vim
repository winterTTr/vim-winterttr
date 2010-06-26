let SessionLoad = 1
if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
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
vmap <silent> <Plug>IMAP_JumpBack `<i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpBack "_<Del>i=IMAP_Jumpfunc('b', 0)
vmap <silent> <Plug>IMAP_DeleteAndJumpForward "_<Del>i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>IMAP_JumpBack i=IMAP_Jumpfunc('b', 0)
nmap <silent> <Plug>IMAP_JumpForward i=IMAP_Jumpfunc('', 0)
nmap <silent> <Plug>CalendarH :cal Calendar(1)
nmap <silent> <Plug>CalendarV :cal Calendar(0)
snoremap <silent> <S-Tab> <Left>F`i=TTrCodeAssistor_Action("b")
nnoremap <silent> <F8> :TlistToggle
nnoremap <silent> <C-F5> :if expand("%:p:h") != "" |execute '!start explorer.exe '.substitute(expand("%:p:h"),'/','\','g')|endif
nnoremap <F7> :echo "hi<".synIDattr(synID(line("."),col("."),1),"name").'> trans<'.synIDattr(synID(line("."),col("."),0),"name")."> lo<".synIDattr(synIDtrans(synID(line("."),col("."),1)),"name").">"
nmap <F11> :set guifont=*
nmap <F10> :set guifont=GB_YuanHei:h12:cGB2312
nmap <F9> :set guifont=Lucida_Sans_Typewriter:h11:cANSI
noremap <F12> :%s/\\u\(\w\w\w\w\)/\=nr2char("0x".expand("<cword>")[1:])/g
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
inoremap  =GetCloseTag()
inoremap <silent> ( =TTrCodeAssistor_CompleteFuncPrototypeFromTags()
inoremap <silent> ) =TTrCodeAssistor_IntelligentRightBracket()
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
set guifont=Lucida_Sans_Typewriter:h11:cANSI
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
set smartindent
set statusline=%<%f%m\ [%{&ff}:%{&fenc}:%Y]\ %{getcwd()}\ \ [%{strftime('%Y/%b/%d\ %a\ %I:%M\ %p')}]\ %=\ Line:%l/%L\ Column:%c%V\ %P
set suffixes=.bak,~,.o,.h,.info,.swp,.obj,.class
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
cd D:\~tmp\~~~~LOOK
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +326 Diff.java
args Diff.java
edit Diff.java
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 30 + 64) / 128)
exe 'vert 2resize ' . ((&columns * 97 + 64) / 128)
argglobal
enew
file __Tag_List__
let s:cpo_save=&cpo
set cpo&vim
inoremap <buffer> <silent> <kMultiply> :silent! %foldopen!
inoremap <buffer> <silent> <kMinus> :silent! foldclose
inoremap <buffer> <silent> <kPlus> :silent! foldopen
nnoremap <buffer> <silent> * :silent! %foldopen!
nnoremap <buffer> <silent> + :silent! foldopen
nnoremap <buffer> <silent> - :silent! foldclose
nnoremap <buffer> <silent> = :silent! %foldclose
nnoremap <buffer> <silent> q :close
nnoremap <buffer> <silent> <kMultiply> :silent! %foldopen!
nnoremap <buffer> <silent> <kMinus> :silent! foldclose
nnoremap <buffer> <silent> <kPlus> :silent! foldopen
inoremap <buffer> <silent> * :silent! %foldopen!
inoremap <buffer> <silent> + :silent! foldopen
inoremap <buffer> <silent> - :silent! foldclose
inoremap <buffer> <silent> = :silent! %foldclose
inoremap <buffer> <silent> q :close
let &cpo=s:cpo_save
unlet s:cpo_save
setlocal noarabic
setlocal autoindent
setlocal autoread
setlocal balloonexpr=Tlist_Ballon_Expr()
setlocal nobinary
setlocal bufhidden=delete
setlocal nobuflisted
setlocal buftype=nofile
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
setlocal expandtab
if &filetype != 'taglist'
setlocal filetype=taglist
endif
setlocal foldcolumn=3
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=9999
setlocal foldmarker={{{,}}}
set foldmethod=marker
setlocal foldmethod=manual
setlocal foldminlines=0
setlocal foldnestmax=20
setlocal foldtext=v:folddashes.getline(v:foldstart)
setlocal formatexpr=
setlocal formatoptions=tcql
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
setlocal nomodifiable
setlocal nrformats=octal,hex
set number
setlocal nonumber
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
if &syntax != 'taglist'
setlocal syntax=taglist
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=72
setlocal thesaurus=
setlocal nowinfixheight
set winfixwidth
setlocal winfixwidth
setlocal nowrap
setlocal wrapmargin=0
wincmd w
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
setlocal cinoptions=j1
setlocal cinwords=if,else,while,do,for,switch
setlocal comments=sr:/*,mb:*,ex:*/,://
setlocal commentstring=//%s
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
if &filetype != 'java'
setlocal filetype=java
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
setlocal includeexpr=substitute(v:fname,'\\.','/','g')
setlocal indentexpr=GetJavaIndent()
setlocal indentkeys=0{,0},:,0#,!^F,o,O,e,0=extends,0=implements
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
setlocal smartindent
setlocal softtabstop=0
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal statusline=
setlocal suffixesadd=.java
setlocal noswapfile
setlocal synmaxcol=3000
if &syntax != 'java'
setlocal syntax=java
endif
setlocal tabstop=4
setlocal tags=
setlocal textwidth=72
setlocal thesaurus=
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal wrap
setlocal wrapmargin=0
let s:l = 401 - ((0 * winheight(0) + 21) / 43)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
401
normal! 0
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 64) / 128)
exe 'vert 2resize ' . ((&columns * 97 + 64) / 128)
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
