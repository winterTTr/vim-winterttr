"   Filename: .vimrc
"   Author: winterTTr
"   Mail: winterTTr@gmail.com
"   Version: $Id: _vimrc 16 2008-11-27 09:58:57Z winterTTr $



"=============================================================================
" Encoding and lang options {{{1
set langmenu=none
set helplang=cn
set fileformats=unix,dos
if has("multi_byte")
    set nobomb
    set encoding=utf-8
    if has("unix")
        set fileencodings=ucs-bom,utf-8,euc-cn,prc,latin1
    endif

    if has("win32")
        set fileencodings=ucs-bom,utf-8,cp932,cp936,cp950,prc,latin1
    endif
else
    echoerr "Sorry,this version of (g)vim was not compiled with +multi_byte"
endif
"}}}1
"=============================================================================
" UI Settings {{{1
"-------------------------------------------------
syntax on
set selection=inclusive
set showmode
set showcmd
set title
set number
set ruler
"set rulerformat=%55(%{strftime('%a\ %b\ %e\ %I:%M\ %p')}\ %5l,%-6(%c%V%)\ %P%)
set showmatch
set visualbell t_vb= 
set novisualbell
"set cul
"set guifont&

" --- Status Line --- {{{2
set laststatus=2
"set statusline=%<%f%m\ \[%{&ff}:%{&fenc}:%Y]\ %{getcwd()}\ \ \[%{strftime('%Y/%b/%d\ %a\ %I:%M\ %p')}\]\ %=Ascii:(%b,0x%B)\ Line:%l\/%L\ Column:%c%V\ %P
set statusline=%<%f%m\ \[%{&ff}:%{&fenc}:%Y]\ %{getcwd()}\ \ \[%{strftime('%Y/%b/%d\ %a\ %I:%M\ %p')}\]\ %=\ Line:%l\/%L\ Column:%c%V\ %P
" ------------------- }}}2

" --- GUI options --- {{{2
if has("gui_running")
    set clipboard=autoselect
    set mousehide
    set columns=130
    set lines=45
    "colorscheme darkblue
	"colorscheme desertEx
    "colorscheme freya
	"colorscheme brookstream
    colorscheme darkerdesert
    set background=dark
    "set guioptions=aegimtrLv
    set guioptions=aegimtrL
    let Tlist_Show_Menu=1
    "set guifont=Bitstream_Vera_Sans_Mono:h10:cANSI
    set guifont=Fixedsys:h10:cGB2312
    "set guifont=Bitstream_Vera_Sans_Mono:h10:b:cANSI
    set guifontwide=NSimsun:h12
endif
" ------------------- }}}2

" --- Folder Option --- {{{2
set foldmethod=marker
" --------------------- }}}2

" --- CommandLine Complete Option --- {{{2
set wildmode=longest,list
set wildmenu
set wildchar&
" ----------------------- }}}2

set confirm

"}}}1
"=============================================================================
" Diff options {{{1
set diffopt=filler,context:6,vertical
" }}}1
"=============================================================================
" Search options {{{1
"-------------------------------------------------
set hlsearch
set incsearch
set ignorecase
set smartcase
set infercase
set wrapscan
"}}}1
"=============================================================================
" Auto options {{{1
"-------------------------------------------------
filetype plugin on
filetype on
set autoread
set autoindent

" --- auto command ---- {{{2
if !exists("autocommands_loaded")
    let autocommands_loaded = 1

	augroup SymbianFileType
		autocmd BufRead,BufNewFile *.hrh set filetype=cpp 
		au!
	augroup END

	autocmd QuickFixCmdPost * cwindow
    autocmd FileType * :set formatoptions=tcql autoindent comments&
    autocmd FileType css :set formatoptions=cql autoindent
    autocmd FileType c,cpp,h,java :set formatoptions=croql smartindent
                \ comments=sr:/*,mb:*,ex:*/,:// expandtab
	"autocmd BufEnter * :cd %:p:h
    "autocmd CursorMoved *.c,*.cpp,*.h,*.java call ColumnHighlight()
    "autocmd InsertEnter *.c,*.cpp,*.h,*.java call RemoveHighlightOnInsertEnter()
    augroup CPPFile "{{{3
        au!
        autocmd FileType cpp syn match cppFuncDef "::\~\?\zs\h\w*\ze([^)]*\()\s*\(const\)\?\)\?$"
                    \| hi def link cppFuncDef Special
    augroup END   " }}}3
    "autocmd GUIEnter * simalt ~x
    " vim -b : edit binary using xxd-format!
    augroup Binary " {{{3
        au!
        au BufReadPre  *.bin,*.exe let &bin=1
        au BufReadPost *.bin,*.exe if &bin | %!xxd
        au BufReadPost *.bin,*.exe set ft=xxd | endif
        au BufRead *.exe,*.bin if &bin | set noendofline | endif
        au BufWritePre *.bin,*.exe if &bin | %!xxd -r
        au BufWritePre *.bin,*.exe endif
        au BufWritePost *.bin,*.exe if &bin | %!xxd
        au BufWritePost *.bin,*.exe set nomod | endif
    augroup END  " }}}3
    augroup TTrSessionManager " {{{3
        au!
        "autocmd VimLeave * call TTr_SessionSave()
        "autocmd VimEnter * call TTr_SessionLoad()
    augroup END  " }}}3
endif
" ---------------------}}}2

"}}}1
"=============================================================================
" Format Options {{{1
"-------------------------------------------------
set display=lastline,uhex
set textwidth=72
set shiftwidth=4
set tabstop=4
"set background=dark
set linebreak
"}}}1
"=============================================================================
" Control options {{{1
"-------------------------------------------------
set backspace=eol,indent,start
set whichwrap=b,s,h,l
set iminsert=1
set imsearch=1
" make it possible to use shift + <array> to select context(select-mode)
set selectmode=key
set keymodel=startsel,stopsel
set switchbuf=useopen,usetab
set winaltkeys=no
"}}}1
"=============================================================================
" Key map {{{1
"-------------------------------------------------

" --- Map the <UP> and <DOWN> ---{{{2
noremap <UP> gk
noremap <DOWN> gj
"--------------------------------}}}2

" --- Close the file via <C-C>--- {{{2
nnoremap <silent> <C-C> :q<CR>
vnoremap <silent> <C-C> <C-C>:q<CR>
inoremap <silent> <C-C> <C-O>:q<CR>
" ------------------------------}}}2

" --- Save the file via <C-S> ---{{{2
function! s:TTr_MapFunc_SaveAction()
	if expand("%") == "" 
		browse confirm update 
	else 
		confirm update 
	endif
endfunction
inoremap <silent> <C-S> <C-O>:call <SID>TTr_MapFunc_SaveAction()<CR>
nnoremap <silent> <C-S> :call <SID>TTr_MapFunc_SaveAction()<CR>
vnoremap <silent> <C-S> <C-C>:call <SID>TTr_MapFunc_SaveAction()<CR>
" -------------------------------}}}2

" --- Open the file in the current directory via <,e>---{{{2
nnoremap ,e :e <C-R>=expand("%:p:h")."\\"<CR>
" ----------------------------------------------}}}2

" --- tag help key ---{{{2
noremap  <M-]>  :tab split<CR><C-]>
nnoremap <space> <C-W>}
"----------------------}}}2

" --- > and < do not affect the V-mode --- {{{2
xnoremap    <   <gv
xnoremap    >   >gv
" ------------------------------------- }}}2

" --- let the / can hl during search and complete --- {{{2
cnoremap    <m-n>   <cr>/<c-r>=histget('/',-1)<cr>
cnoremap    <m-i>   <c-r>=substitute(getline('.')[(col('.')-1):],'\W.*','','g')<cr>
" --------------------------------------------------- }}}2

" --- HiaHia if you can know --- {{{2
"noremap <F12> :%s/\\u\(\w\w\w\w\)/\=nr2char("0x".expand("<cword>")[1:])/g<CR>
" ------------------------------ }}}2

" --- Scroll using <C-J> and <C-K> --- {{{2
nnoremap    <C-J>   <C-E>
nnoremap    <C-K>   <C-Y>
" ------------------------------------ }}}2

" --- [CTRL-hjkl to browse command history and move the cursor] --- {{{2
cnoremap    <C-K>   <up>
cnoremap    <C-J>   <down>
cnoremap    <C-H>   <left>
cnoremap    <C-L>   <right>
" ----------------------------------------------------------------- }}}2

" --- [CTRL-hjkl to move the cursor in insert mode --- {{{2
inoremap    <C-K>   <up>
inoremap    <C-J>   <down>
inoremap    <C-H>   <left>
inoremap    <C-L>   <right>
" ---------------------------------------------------- }}}2

" --- Change the fonds via <F9> <F10> <F11>--- {{{2
"nmap <F9> :set guifont=Lucida_Sans_Typewriter:h11:cANSI<CR>
"nmap <F10> :set guifont=GB_YuanHei:h12:cGB2312<CR>
"nmap <F11> :set guifont=*<CR>
" ---------------------------------- }}}2

" --- <M-/> no highlight :nohl --- {{{2
nnoremap <silent> <M-/> :nohl<CR>
" -------------------------------- }}}2

" --- Get the current highlight group --- {{{2
nnoremap  <F7>  :echo "hi<".synIDattr(synID(line("."),col("."),1),"name").'> trans<'.synIDattr(synID(line("."),col("."),0),"name")."> lo<".synIDattr(synIDtrans(synID(line("."),col("."),1)),"name").">"<CR>
" --------------------------------------- }}}2

" --- Find the line with the same indent --- {{{2
nn <M-,> k:call search ("^". matchstr (getline (line (".")+ 1), '\(\s*\)') ."\\S", 'b')<CR>^
nn <M-.> :call search ("^". matchstr (getline (line (".")), '\(\s*\)') ."\\S")<CR>^
" ------------------------------------------ }}}2

" --- Use <M-j> <M-k> to move between each tab --- {{{2
"nnoremap <m-j> gt
"nnoremap <m-k> gT
"inoremap <m-j> <C-O>gt
"inoremap <m-k> <C-O>gT
" ------------------------------------------------ }}}2

" --- Folder after Search --- {{{2
nnoremap <silent> <leader>z :set foldexpr=getline(v:lnum)!~@/ foldlevel=0 foldcolumn=0 foldmethod=expr<CR>
" --------------------------- }}}2

" --- Toggle between the fold open and close with <cr> --- {{{2
nnoremap <CR> :call TTr_ToggleFold()<CR>
" -------------------------------------------------------- }}}2

" --- Let the paste to auto indent --- {{{2
nnoremap p pmz=`]`z
nnoremap <c-p> p
" ------------------------------------ }}}2

" --- Open with EmEditor --- {{{2
"nnoremap <F9>  execute '! start "EmEditor" "C:\Program Files\EmEditor\EmEditor.exe" '.substitute(expand("%:p"),'/','\','g')<CR>
" ------------------------------------ }}}2

" -- Open the current files directory and command line here --- {{{2
if has("gui_running")
    if has("win32")
        " Open the folder containing the currently open file. Double <CR> at end
        " is so you don't have to hit return after command. Double quotes are
        " not necessary in the 'explorer.exe %:p:h' section.
        nnoremap <silent> <C-F5> :if expand("%:p:h") != "" \|execute '!start explorer /e,/select,'.substitute(expand("%:p"),'/','\','g')\|endif<CR>
        nnoremap <silent> <C-F6> :execute '!start cmd.exe /k cd /d "' . expand("%:h") . '"'<CR>
    endif
endif
" --------------------------------------- }}}2

"}}}1
"=============================================================================
" ETC options {{{1
set nocompatible
set nobackup
set noswapfile
set history=100
lang message en_US
"}}}1
"=============================================================================
" Abbreviations {{{1
""--------------------------------------------------
" See from the TTrCodeAssistor.vim which is wroten by me. :-)
let g:TTrCodeAssistor_AutoStart=0
""}}}1
"=============================================================================
" Cscope Options and map {{{1

" --- Options --- {{{2
if has("cscope")
    set csprg=cscope
    set cscopetag
    set cscopequickfix=c-,d-,e-,f-,g-,i-,s-,t-
    set cscopetagorder=0  " Using cscope first
    set nocscopeverbose
    if filereadable("cscope.out")
        cs add cscope.out
    elseif $CSCOPE_DB != ""
        cs add $CSCOPE_DB
    endif
    set cscopeverbose
endif
" --------------- }}}2

" --- Key Map -- {{{2
"   0 or s: Find this C symbol
"   1 or g: Find this definition
"   2 or d: Find functions called by this function
"   3 or c: Find functions calling this function
"   4 or t: Find this text string
"   6 or e: Find this egrep pattern
"   7 or f: Find this file
"   8 or i: Find files #including this file
nmap gns :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap gng :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap gnc :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap gnt :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap gne :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap gnf :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap gni :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap gnd :cs find d <C-R>=expand("<cword>")<CR><CR>

nnoremenu <silent> &Cscope.symbol :cs find s <C-R>=expand("<cword>")<CR><CR>
nnoremenu <silent> &Cscope.definition :cs find g <C-R>=expand("<cword>")<CR><CR>
nnoremenu <silent> &Cscope.call\ function :cs find c <C-R>=expand("<cword>")<CR><CR>
nnoremenu <silent> &Cscope.calling\ function :cs find t <C-R>=expand("<cword>")<CR><CR>
nnoremenu <silent> &Cscope.text :cs find e <C-R>=expand("<cword>")<CR><CR>
nnoremenu <silent> &Cscope.egrep\ pattern :cs find f <C-R>=expand("<cfile>")<CR><CR>
nnoremenu <silent> &Cscope.file :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nnoremenu <silent> &Cscope.including\ file :cs find d <C-R>=expand("<cword>")<CR><CR>
" ------------------------ }}}2

"}}}1
"=============================================================================
" taglist options {{{1
nnoremap <silent><F8> :TlistToggle<CR>
let Tlist_Use_SingleClick=0
let Tlist_Use_Right_Window = 1
let Tlist_File_Fold_Auto_Close = 1
let Tlist_Exit_OnlyWindow=1
let updatetime=4
let Tlist_Sort_Type="name"
" }}}1
"=============================================================================
" quick buffer options {{{1
let g:qb_hotkey = '<M-l>'
" }}}1
"=============================================================================
" Commands {{{1
command!    -nargs=0 CPPtags        !ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .
command!    -nargs=0 Vimrc          tabedit $MYVIMRC
command!    DiffOrig         vert new | set bt=nofile | r # | 0d_ | diffthis | wincmd p | diffthis

command!    -nargs=0 ShowFunctions  call TTr_ShowProgrammingTags('f')
command!    -nargs=0 ShowDefines  call TTr_ShowProgrammingTags('d')
command!    -nargs=0 ShowClasses  call TTr_ShowProgrammingTags('c')

command!    -nargs=+ -complete=command Fs call TTr_Foldsearch(<q-args>)
command!    -nargs=0 Japi Fs public\|protected\|private

command!    -nargs=0 FoldNoArea set foldexpr=getline(v:lnum)!~@/ foldlevel=0 foldcolumn=0 foldmethod=expr

"--style=ansi --indent=spaces=4 --brackets=break --indent-switches --indent-namespaces
"--max-instatement-indent=40 --min-conditional-indent=40 --break-blocks --pad=paren-in --convert-tabs
"--indent-preprocessor
command!    -nargs=0 Astyle !astyle --style=ansi -s4 -b -S -N -M -m -D -V --indent-preprocessor %

command!    -nargs=0 HideFunctions call TTr_HideAll()

command!    -nargs=1 SetSession :let g:SessionFileName=g:PathToSessions.<q-args>.".vim"
command!    -nargs=1 UnsetSession :let g:SessionFileName=""

command!    -nargs=1 -complete=dir TagsSetPath call <SID>TTr_AutoTags_SetLocalPath(<f-args>)
" }}}1
"=============================================================================
" Functions For Mine :-) {{{1

" --- Switch Between the java/cpp/c and its h files --- {{{2
nnoremap    <silent> <M-o>   :call SwitchBetweenProgrammingFile()<CR>

" Function <SwitchBetweenProgrammingFile> used to detect the file .{{{3
"       if exist , split open ; else ask to create.
function! SwitchBetweenProgrammingFile() "{{{4

    " Open type ( now I set it to vertical split )
    let FileOpenType = "vertical split "
    "let FileOpenType = "tabnew "

    " get Current file's expand name and the name without exp including the full path
    let CurExpName = expand("%:e")
    let CurFullPathNameNoExp = expand("%:p:r")
    let CurNameNoExp = expand("%:r")

    " Make the list for detecting when the current file is H file
    let ExpIndex = ["cpp","c","java",""]

    " if the CurExpName == H , detecting the possible file and open the first can be readable
    if CurExpName == "h"
        "detecting
        for index in ExpIndex
            let FullNameForOpen = CurFullPathNameNoExp.".".index
            if filereadable(FullNameForOpen)
                execute FileOpenType.FullNameForOpen
                return
            endif
        endfor
        " if can't find one , ask to create
        let UserInputExpName = input("create file (<esc> to cancel): ".CurNameNoExp.".",&filetype)
        if UserInputExpName == ""
            "execute FileOpenType.CurFullPathNameNoExp
            return
        else
            execute FileOpenType.CurFullPathNameNoExp.".".UserInputExpName
            return
        endif
    endif
    
    " if the CurExpName != h , open the H file if exist.
    if filereadable(CurFullPathNameNoExp.".h")
        execute FileOpenType.CurFullPathNameNoExp.".h"
        return
    else " not exsit , ask to create
        let UserChoice = input("Create file [".CurNameNoExp.".h] ?[y/n]","y")
        if UserChoice == "y"
            execute FileOpenType.CurFullPathNameNoExp.".h"
            return
        else " not y
            return
        endif
    endif

endfunction "}}}4
" end function SwitchBetweenProgrammingFile }}}3
" ------------------------------------------------------ }}}2

" --- TTr_ShowProgrammingTags() from VimTips --- {{{2
function! TTr_ShowProgrammingTags(type)
    if a:type == 'f'
        let typeString = 'function'
    elseif a:type == 'd'
        let typeString = 'macro'
    elseif a:type == 'c'
        let typeString = 'class'
    endif


    let gf_s = &grepformat
    let gp_s = &grepprg

    let &grepformat = '%*\k%*\s'.typeString.'%*\s%l%*\s%f %*\s%m'
    let &grepprg = 'ctags -x --c-types='.a:type.' --c++-types='.a:type.' --sort=no -o -'

    write
    silent! grep %
    cwindow

    let &grepformat = gf_s
    let &grepprg = gp_s
endfunction
" ----------------------------------- }}}2

" --- FoldSearch() from VimTips --- {{{2
function! TTr_Foldsearch(search)
    echohl WarningMsg | echo "setlocal fm=manual" | echohl None
    setlocal foldmethod=manual
    silent! normal zE
    silent! normal G$
    let folded = 0     "flag to set when a fold is found
    let flags = "w"    "allow wrapping in the search
    let line1 =  0     "set marker for beginning of fold
    while search(a:search, flags) > 0
        let  line2 = line(".")
        if (line2 -1 > line1)
            execute ":" . line1 . "," . (line2-1) . "fold"
            let folded = 1       "at least one fold has been found
        endif
        let line1 = line2     "update marker
        let flags = "W"       "turn off wrapping
    endwhile
    " Now create the last fold which goes to the end of the file.
    normal $G
    let  line2 = line(".")
    if (line2  > line1 && folded == 1)
        execute ":". line1 . "," . line2 . "fold"
    endif
    normal gg0
endfunction
" --------------------------------- }}}2

" --- HighLight column matching (from mbbill)--- {{{2
let g:TTr_ShowHighlightColumn=0
function! ColumnHighlight()
    let c=getline(line('.'))[col('.') - 1]
    if c=='{' || c=='}'
        set cuc
        let g:TTr_ShowHighlightColumn=1
    else
        if g:TTr_ShowHighlightColumn==1
            set nocuc
            let g:TTr_ShowHighlightColumn=0
        endif
    endif
endfunction
function! RemoveHighlightOnInsertEnter()
    if g:TTr_ShowHighlightColumn == 1
        set nocuc
    endif
endfunction
" --------------------------------- }}}2

" --- toggle the fold with one key <cr> -- {{{2
function! TTr_ToggleFold()
    if foldlevel('.') == 0
        normal! j
    else
        if foldclosed('.') < 0
            . foldclose
        else
            . foldopen
        endif
    endif
    " Clear status line
    echo
endfunction
" ---------------------------------------- }}}2

" --- Hide the function --- {{{2
function! TTr_HideAll()
    syn region HideFunctionRegion start="{" end="}" transparent fold
    syn sync fromstart
    "set foldnestmax=1
    set foldmethod=syntax
endfunction
" ------------------------- }}}2

" --- Load and Save Session --- {{{2
let g:SessionFileName=""
if has("win32")
    let g:PathToSessions = substitute($VIM,'\','/','g')."/sessions/"
else
    let g:PathToSessions = $HOME."/.vim/sessions/"
endif
function! TTr_SessionLoad()
    if argc() == 0
        " gvim started with no files
        if has("browse") == 1
            let g:SessionFileName = browse(0, "Select Session", g:PathToSessions, "LastSession.vim")
            if g:SessionFileName != ""
                exe "source " . g:SessionFileName
            endif
        else
            " For non-gui vim
            let LoadLastSession = confirm("Restore last session?", "&Yes\n&No")
            if LoadLastSession == 1
                exe "source " . g:PathToSessions . "LastSession.vim"
            endif
        endif
    endif
endfunction
function! TTr_SessionSave()
   exe "mksession! " . g:PathToSessions . "LastSession.vim"
   if exists("g:SessionFileName") == 1
      if g:SessionFileName != ""
         exe "mksession! " . g:SessionFileName
      endif
   endif
endfunction
" ------------------------------ }}}2

" --- Toggle Comments --- {{{2

"nnoremap <F7> :call TTrCodeAssistor_ToggleComments()<CR>
"vnoremap <F7> :call TTrCodeAssistor_ToggleComments()<CR>
" ----------------------- }}}2

" --- Auto update Tags File when save --- {{{2
let g:TTr_AutoTags_Config = {}
let g:TTr_AutoTags_Config['global'] = ['D:\SymbianSDK\taglist\SDK\tags']
let g:TTr_AutoTags_Config['local'] = ""

function! s:TTr_AutoTags_SetLocalPath(tagsPath)
	let g:TTr_AutoTags_Config['local'] = a:tagsPath
	set tags=
	for gpath in g:TTr_AutoTags_Config['global']
		execute "set tags+=" . gpath
	endfor
	execute "set tags+=" . g:TTr_AutoTags_Config['local'].'*.tags'
endfunction

function! s:TTr_AutoTags_UpdateTagsFiles()
	" check auto save path
	if !exists("g:TTr_AutoTags_Config") || g:TTr_AutoTags_Config['local'] == ""
		return
	endif

	" check if the buffer associated with a file
	if expand("%:p") == ""
		return
	endif

	let tagsOutputFile = g:TTr_AutoTags_Config['local'] . expand("%:p:t") .'.tags'
	let tagsTargetFile = expand("%:p")
	let execCmd = '!ctags --c++-kinds=+p --fields=+iaS --extra=+q -f "'. tagsOutputFile . '" "' . tagsTargetFile .'"'
	silent execute execCmd
endfunction

" ----------------------- }}}2

" [AutoComplete functions] from mbbill {{{2
"let s:min_len = 2
"function! AutoComplete()
"    let length = strlen(matchstr(getline('.')[:col('.')-2],'\w*$'))
"    if length != s:min_len
"        return ''
"    else
"        return "\<c-x>\<c-n>\<c-p>"
"    endif
"endfun
"function! DoAutoComplete()
"    let letter = char2nr("a")
"    while letter <= char2nr("z")
"        execute "inoremap <buffer>" nr2char(letter) nr2char(letter) . "<c-r>=AutoComplete()<CR>"
"        let letter = letter + 1
"    endwhile
"    let letter = char2nr("A")
"    while letter <= char2nr("Z")
"        execute "inoremap <buffer>" nr2char(letter) nr2char(letter) . "<c-r>=AutoComplete()<CR>"
"        let letter = letter + 1
"    endwhile
"endfun
"
"autocmd BufReadPost * call DoAutoComplete() "}}}2


"}}}1
"=============================================================================
" Python {{{1

function! Py_CompleteAttributes() "{{{2
    "let ModulePath = matchstr(getline(".")[:col('.')],'\m[0-9A-Za-z.]*\.\w*$')
	"let partName = matchstr(getline("."),'\m[0-9A-Za-z.]*\.\zs\w*\ze.*$')
    redir => AttrNameStr | silent exec "py print getAttributesByName()" | redir END

    let AttrNameStr = AttrNameStr[1:]
    let AttrNameList = split(AttrNameStr,',')

    if len(AttrNameList) == 1 || len(AttrNameList) == 0 
        return ""
    endif

    let offset = AttrNameList[0] + 0

    let AttrNameListDict = []
    for item in AttrNameList[1:]
        let AttrName = matchstr( item , '\m\zs.*\ze!.*' )
        let AttrType = matchstr( item , '\m.*!\zs.*\ze' )
        call add( AttrNameListDict , {'word': AttrName , 'menu':AttrType })
    endfor

    call complete(col('.') - offset , AttrNameListDict)

    return ""
endfunction "}}}2

if !exists("autoload_python") "{{{2
    let autoload_python = 1
    augroup PYTHON
        au!
        autocmd FileType PYTHON set expandtab shiftwidth=4
        "autocmd FileType PYTHON inoremap <C-ENTER> <C-R>=Py_CompleteAttributes()<CR>

	   "Set some bindings up for 'compile' of python
	   autocmd FileType python set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
	   autocmd FileType python set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m

    augroup END
endif "}}}2

" }}}1
"=============================================================================
" Doxygen {{{1

" DgFileHeader {{{2
function! DgExpandFileHeader() "{{{ 2
	let DgFileHeader = [ 
				\' *  \brief    -->add brief <--',
				\' *  \author   winterTTr',
				\' *  \version  $Revision$',
				\' *  \date     $Date$' , 
				\' *  \bug      --> add bug list <--',
				\' *',
				\' *  --> add detail msg here --<',
				\' */']
	let fileName = expand('%:t')
	call insert( DgFileHeader , '/*! \file     '.fileName , 0 )
	call append( 0 , DgFileHeader )
endfunction "}}}2
command! -nargs=0 DgFile call DgExpandFileHeader()

function! DgExpandFunctionHeader() "{{{2
    let curLineNumber = line('.')
    let curLineContent = getline('.')

    let doxygenContent = []

    " add \fn
    let functionDeclaration = substitute(curLineContent ,';','','g')
    call add( doxygenContent , '/*! \fn       ' . functionDeclaration)
    
    let paramStr = matchstr( functionDeclaration , '\m(\zs[^)]*\ze)' )
    let eachPartList = split( paramStr , ',' )


    " analyze each param name 
    let paramNameList = []
    if 1 == len(eachPartList) && 0 == len( substitute( eachPartList[0] , ' ','' , 'g') )
        let paramNameList = []
    else
        for eachItem in eachPartList
            call add( paramNameList , matchstr( eachItem , '\m\zs\w\+\ze\ *$') )
        endfor
    endif


    " add \param
    if 0 != len(paramNameList )
        for eachItem in paramNameList
            call add( doxygenContent , ' *  \param[in,out]   ' . eachItem . '    --> add comment <--')
        endfor
    endif

    " add \return and detail message
    call add ( doxygenContent , ' *  \return   --> add comment <--')
    call add ( doxygenContent , ' *')
    call add ( doxygenContent , ' *  --> add detail msg <--')
    call add ( doxygenContent , ' */')


    call append( curLineNumber - 1 , doxygenContent )
endfunction "}}}2
command! -nargs=0 DgFunction call DgExpandFunctionHeader()

function! DgExpandClassHeader( type ) "{{{2
    let doxygenContent = []
    let curLineContent = getline('.')
    let curLineNumber = line('.')

    "get Class name
    let className = matchstr(curLineContent , a:type . '\ \+\zs\w\+\ze')
    if 0 == len(className)
        echohl WarningMsg | echo "Can't find Class identifier in current line ." | echohl None
        return
    endif

    call add(doxygenContent , '/*! \'.a:type. repeat( ' ' , 9 - len(a:type) ) . className)

    call add(doxygenContent , ' *  \brief    --> add brief <--')
    call add(doxygenContent , ' *')
    call add(doxygenContent , ' *  --> add detail msg <--')
    call add(doxygenContent , ' */')

    call append(curLineNumber-1 , doxygenContent)
endfunction "}}}2
command! -nargs=0 DgClass    call DgExpandClassHeader('class')
command! -nargs=0 DgStruct    call DgExpandClassHeader('struct')

function! DgExpandDefineHeader() "{{{2
    let doxygenContent = []
    let curLineNum = line('.')
    let curLineContent = getline('.')

    let defName = matchstr( curLineContent , '\m#define\W\+\zs\w\+\ze' )
    
    call add(doxygenContent , '/*! \def      ' . defName)
    call add(doxygenContent , ' *  --> about define <---')
    call add(doxygenContent , ' */')

    call append(curLineNum -1 , doxygenContent)
endfunction "}}}2
command! -nargs=0 DgDefine  call DgExpandDefineHeader()

command! -nargs=0 DgMember  execute "normal A\<tab>\<tab>/*!<   */\<left>\<left>\<left>" | startinsert

" }}}1
"=============================================================================
" Latex Setting {{{1
if has("win32")
    set shellslash
endif
augroup LatexSuite
    autocmd!
    autocmd FileType TEX :set sw=2 iskeyword+=:
augroup end
filetype indent on
set grepprg=grep\ -nH\ $*
" }}}1
"=============================================================================
" Menu {{{1
"menu <silent> TT&r.&Edit\ Vimrc :Vimrc<CR>
"menu <silent> TT&r.&Select\ Fonts\.\.\. :set guifont=*<CR>
"menu <silent> TT&r.-sep1-       :
"menu <silent> TT&r.HideNoArea   :FoldNOArea<CR>
"menu <silent> TT&r.-sep2-       :
"menu <silent> TT&r.&Programming.&CPPTags<tab>:CPPTags :CPPtags<CR>
"menu <silent> TT&r.&Programming.&Astyle<tab>:Astyle :Astyle<CR>
"menu <silent> TT&r.&Programming.&HideFunction<tab>:HideFunctions :HideFunctions<CR>
"menu <silent> TT&r.&Programming.&ShowFunction<tab>:ShowFunctions :ShowFunctions<CR>
"menu <silent> TT&r.&Programming.&ShowDefine<tab>:ShowDefines :ShowDefines<CR>
"menu <silent> TT&r.&Programming.&ShowClass<tab>:ShowClasses :ShowClasses<CR>
"menu <silent> TT&r.&Programming.&JavaApi<tab>:Japi :Japi<CR>
"menu <silent> TT&r.&Utilities.&Toggle\ Sketch :call ToggleSketch()<CR>
"menu <silent> TT&r.&Utilities.&Matrix<tab>:Matrix :Matrix<CR>
"menu <silent> TT&r.&Utilities.&Calendar<tab>:Calendar :Calendar<CR>

" }}}1
"=============================================================================
" Tips ;o) {{{1
" Let Vim to be the man viewer{{{2
"sh, ksh:  export MANPAGER="col -b | view -c 'set ft=man nomod nolist' -" }}}2
" }}}1
"=============================================================================


" vim: set ft=vim ff=unix tw=72 foldmethod=marker :

