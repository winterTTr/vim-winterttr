let vlib#buffer#CCommandTarget = vlib#operator#New()

function vlib#buffer#CCommandTarget.Init() dict
	let self.mCommandQueue = []
endfunction


function vlib#buffer#CCommandTarget.DoCommands() dict
	let queue = self.mCommandQueue
	while len( queue ) != 0
		let cmd = remove( queue , 0 )
		execute cmd
	endwhile
endfunction

function vlib#buffer#CCommandTarget.RegisterCommand(aCommand,aForceRun) dict
	call insert( self.mCommandQueue , a:aCommand , len( queue ) )
	if a:aForceRun
		call vlib#operator#Invoke( self , "DoCommands" )
	endif
endfunction



" define normal buffer, which is used to load file
let vlib#buffer#CBufferBase = vlib#operator#New(g:vlib#buffer#CCommandTarget)

function vlib#buffer#CBufferBase.Init() dict
	" init command target
	call call( g:vlib#buffer#CCommandTarget.Init , [] , self )

	" set buffer id
	self.mBufferID = 0 
endfunction

function vlib#buffer#CBufferBase.DoCommands() dict
	let currentWinID = winnr()

	if !vlib#operator#Invoke( self , "SetFocus" ) | return | endif
	call call( vlib#buffer#CCommandTarget.DoCommands , [] , self )

	execute currentWinID . "wincmd w"
endfunction


function vlib#buffer#CBufferBase#SetFocus() dict
	let winID = bufwinnr( self.mBufferID )
	if winID == -1 | return 0 | endif
	execute winID . "wincmd w"
	return 1
endfunction





