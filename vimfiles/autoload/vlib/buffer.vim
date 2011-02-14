let vlib#buffer#CCommandTarget = vlib#operator#New()

function vlib#buffer#CCommandTarget.Init() dict
	call vlib#operator#Set( self , "mCommandQueue" , [] )
endfunction

function vlib#buffer#CCommandTarget.BeforeDoCommands() dict
	return 1
endfunction

function vlib#buffer#CCommandTarget.AfterDoCommands() dict
	return 1
endfunction

function vlib#buffer#CCommandTarget.DoCommands() dict
	if !vlib#operator#Invoke( self , "BeforeDoCommands" ) | return | endif

	let queue = vlib#operator#Get( self , "mCommandQueue" )
	while len( queue ) != 0
		let cmd = remove( queue , 0 )
		execute cmd
	endwhile
	call vlib#operator#Invoke( self , "AfterDoCommands" )
endfunction

function vlib#buffer#CCommandTarget.RegisterCommand(aCommand,aForceRun) dict
	let queue = vlib#operator#Get( self , "mCommandQueue" )
	call insert( queue , a:aCommand , len( queue ) )
	if a:aForceRun
		call vlib#operator#Invoke( self , "DoCommands" )
	endif
endfunction



" define normal buffer, which is used to load file
let vlib#buffer#CFileBuffer = vlib#operator#New(g:vlib#buffer#CCommandTarget)

function vlib#buffer#CFileBuffer.Init(aFilename) dict
	" init command target
	call vlib#operator#PInvoke( self , "Init" )

	let bufferID = bufnr(a:aFilename,1)
	call vlib#operator#Set( self , "mBufferID" , bufferID )
endfunction


