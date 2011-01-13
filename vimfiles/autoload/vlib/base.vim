function! vlib#base#Init()
	" now we can not call object function directly, use this function to
	" force vim to load script one time, after that , and we can  call
	" object member function , so this function need to do nothing 
endfunction


let vlib#base#object = {}
let vlib#base#object.prototype = {}


function vlib#base#CallWithScope(fname,paramList,scope,this)
	let FuncRef = get( a:scope , a:fname )
	if type( FuncRef ) == g:vlib#type#function
		return call( FuncRef , a:paramList , a:this )
	elseif has_key( a:scope , "prototype") && type( a:scope.prototype ) == g:vlib#type#dict
		return vlib#base#CallWithScope( a:fname , a:paramList , a:scope.prototype , a:this )
	endif

	throw "No such function found"
endfunction

function vlib#base#object.Call(fname,paramList) dict
	return vlib#base#CallWithScope( a:fname , a:paramList , self , self )
endfunction


function vlib#base#object.New() dict
	let newObject = {}
	if has_key( self , 'prototype' ) && type( self.prototype ) == g:vlib#type#dict
		" if we use new, every instance share the same prototype object
		let newObject.prototype = self.prototype
	endif

	for key in keys( self )
		if key == "prototype"
			continue
		endif
		let newObject[key] = deepcopy( self[key] )
	endfor
	return newObject
endfunction

function vlib#base#object#NewClass() dict
	let newObject = {}
	if has_key( self , 'prototype' ) && type( self.prototype ) == g:vlib#type#dict
		" if we NewClass, we deep copy protype, and make sure the new
		" class modification to prototype will not effect inherited
		" class
		let newObject.prototype = deepcopy( self.prototype )
	endif

	for key in keys( self )
		if key == "prototype"
			continue
		endif
		let newObject[key] = deepcopy( self[key] )
	endfor
	return newObject
endfunction





