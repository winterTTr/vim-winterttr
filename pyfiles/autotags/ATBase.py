import vim
import subprocess

class ATTypeBase:
    def __init__( self ):
        augroupname = 'autotags_' + self.GetTypeID().lower()

        vim.command( 'augroup   ' + augroupname )
        vim.command( 'autocmd!' )
        vim.command( 'augroup   END' )

        autocmdFormat = 'autocmd %(group)s %(event)s %(pattern)s %(cmd)s'

        formatDict = {}
        formatDict['group'] = augroupname
        formatDict['pattern'] = ','.join( [ '*.'+ x for x in self.GetFilePattern() ] )

        # BufEnter
        formatDict['event'] = 'BufEnter'
        formatDict['cmd']   = 'py autotags.LoadConfig("' + self.GetTypeID() + '")' 
        vim.command( autocmdFormat % formatDict )

        # BufLeave
        formatDict['event'] = 'BufLeave'
        formatDict['cmd']   = 'py autotags.ResetConfig("' + self.GetTypeID() + '")'
        vim.command( autocmdFormat % formatDict )


        # BufWritePost
        formatDict['event'] = 'BufWritePost'
        formatDict['cmd']   = 'py autotags.UpdateTags("' + self.GetTypeID() + '")'
        vim.command( autocmdFormat % formatDict )

    def GenTags( self , src , dst ):
        subprocess.Popen(  self.GetTagsCommand() % { 'src':src , 'dst': dst } , shell = True )

    # virtual Function , should be implement
    def GetTypeID( self ):
        raise RuntimeError( 'virtual function [GetTypeID]' )

    def GetFilePattern( self ):
        raise RuntimeError( 'virtual function [GetFilePattern]' )

    def GetTagsCommand( self ):
        raise RuntimeError( 'virtual function [GetTagsCommand]' )


    def LoadConfig( self ):
        raise RuntimeError( 'virtual function [LoadConfig]' )


    def ResetConfig( self ):
        raise RuntimeError( 'virtual function [ResetConfig]' )

    def CreateRepository( self ):
        raise RuntimeError( 'virtual function [ResetConfig]' )

    def RemoveRepository( self ):
        raise RuntimeError( 'virtual function [ResetConfig]' )





