" the base class of all the object in vlib, which do not have
" __prototype__ property
let vlib#operator#object = {}

function vlib#operator#New(...)
	let newObject = {}
	if a:0 == 0 
		" a new class from object
		let newObject.__prototype__ = g:vlib#operator#object
	else
		" just use single inheritation
		let newObject.__prototype__ = a:1
	endif
	return newObject
endfunction

function vlib#operator#Invoke(aObject,aFuncName,...)
    return s:CallWithScope(a:aFuncName,a:000,a:aObject,a:aObject)
endfunction

function s:CallWithScope(aFuncName,aParamList,aScope,aSelf)
    let FuncRef = get( a:aScope , a:aFuncName )
    if type( FuncRef ) == g:vlib#type#function
        return call( FuncRef , a:aParamList , a:aSelf )
    else
        let prototype = get( a:aScope , "__prototype__" )
		" not a empty dict, which is vlib#operator#object
        if type( prototype ) == g:vlib#type#dict && len( prototype ) != 0
            return s:CallWithScope( a:aFuncName , a:aParamList , prototype , a:aSelf )
        else
            throw "vexception:No such function:" . a:aFuncName
        endif
    endif
endfunction


