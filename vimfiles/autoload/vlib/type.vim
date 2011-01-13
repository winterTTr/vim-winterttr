function! vlib#type#Init()
	" now we can not call object function directly, use this function to
	" force vim to load script one time, after that , and we can  call
	" object member function , so this function need to do nothing 
endfunction



let vlib#type#number   = type(0)
let vlib#type#string   = type("")
let vlib#type#function = type( function("tr") )
let vlib#type#list     = type( [] )
let vlib#type#dict     = type( {} )
let vlib#type#float    = type( 0.0 )
