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

function vlib#operator#PInvoke(aObject,aFuncName,...)
	let parent = get( a:aObject, "__prototype__" )
	if type( parent ) != g:vlib#type#dict 
		throw "vexception:No such function:" . a:aFuncName
	endif
	return s:CallWithScope(a:aFuncName,a:000,parent,a:aObject)
endfunction


function vlib#operator#Get(aObject,aPropertyName)
	return s:GetWithScope(a:aPropertyName,a:aObject)
endfunction

function vlib#operator#Set(aObject,aPropertyName,aValue)
	let a:aObject[a:aPropertyName] = a:aValue
endfunction


function s:GetWithScope(aPropertyName,aScope)
	if has_key( a:aScope , a:aPropertyName )
		return get( a:aScope , a:aPropertyName )
	else
		let prototype = get( a:aScope , "__prototype__" )
		if type( prototype ) == g:vlib#type#dict && empty(prototype) != 1
			return s:GetWithScope(a:aPropertyName,prototype)
		else
			throw "vexception:No such property:" . a:aPropertyName
		endif
	endif
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


