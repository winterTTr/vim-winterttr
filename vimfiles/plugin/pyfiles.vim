"        File: pyfiles.vim
"     Authors: winterTTr <winterTTr.vim@gmail.com>
"  UpdateDate: 2009-09

" Description: auto load python entry from 'pyfile' folder
"
"     Porpose: make python usage more effectively and conviniently


" check python support
if !has('python')
	echoe "pyfiles requires the vim compile with python support!"
	finish
endif

" check if loaded before
if exists('g:pyfiles_loaded')
	finish
endif
let g:pyfiles_loaded = 1


" check if the base folder exists
if !exists( "g:pyfiles_basepath" )
	let g:pyfiles_basepath = $VIM . '/pyfiles'
endif
if !isdirectory( g:pyfiles_basepath )
	echomsg "pyfiles base folder does not exist , load nothing"
	finish
endif

" check if the init.py exist
let s:pyfiles_init_py = g:pyfiles_basepath . '/init.py'
if !filereadable( s:pyfiles_init_py )
	echomsg " init.py under [" . g:pyfiles_basepath ."] does not exist , load nothing"
	finish
endif

let s:cpo_save = &cpo
set cpo&vim
execute "pyfile " . s:pyfiles_init_py
let &cpo = s:cpo_save
