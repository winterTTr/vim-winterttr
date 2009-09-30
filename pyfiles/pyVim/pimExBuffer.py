from pimWrap import pimBuffer 
from pimWrap import PIM_BUF_TYPE_NORMAL , PIM_BUF_TYPE_READONLY


class pimKeymapBuffer( pimBuffer ):
    def __init__( self , type = PIM_BUF_TYPE_NORMAL , name = None ):
        pimBuffer.__init__( type , name )

        
    def firstEnterHook( self ):
        pass
