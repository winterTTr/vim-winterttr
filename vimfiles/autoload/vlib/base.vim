let vlib#base#NumberType   = type(0)
let vlib#base#StringType   = type("")
let vlib#base#FunctionType = type( function("tr") )
let vlib#base#ListType     = type( [] )
let vlib#base#DictType     = type( {} )
let vlib#base#FloatType    = type( 0.0 )


let vlib#base#object = {}
let vlib#base#object.prototype = {}

"function vlib#base#object.Call(fname,paramList) dict
"	let funcRef = get( self , a:fname )
"	if type( funcRef ) == vlib#base#FunctionType 
"		return call( funcRef , a:paramList , self )
"	endif
"
"	let funcRef = get( self.prototype , a:fname )
"	if type( funcRef ) == vlib#vbase#FunctionType 
"		return call( funcRef , a:paramList , self )
"	endif
"
"	throw "Invalid invoke call, function not exist or no function matched"
"endfunction


function vlib#base#object.New() dict
	echo vlib#base#DictType
	"let newObject = {}
	"echo type( self.prototype )
	"if has_key( self , 'prototype' ) && type( self.prototype ) == vlib#base#DictType
	"	let newObject.prototype = self.prototype
	"endif

	"for key in keys( self )
	"	if key == "prototype"
	"		continue
	"	endif
	"	let newObject[key] = deepcopy( self[key] )
	"endfor
	"return newObject
endfunction





