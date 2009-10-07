from pyVim.pvWrap import pvWindowManager
from pyVim.pvExBuffer import pvListBuffer

class Application:
    def __init__( self ):
        self.winmgr = pvWindowManager('(-,-)main | ( 30 , - )panel , ( -,10) list ')

    def start( self ):
        self.winmgr.makeWindows()

        self.tabnamelist = pvListBuffer()
        self.tabnamelist.showBuffer( self.winmgr.getWindow('list') )

        self.tabnamelist.data = ['complete' , 'buffer list' , 'file explorer' , '123' ]
        self.tabnamelist.updateBuffer( selection = 1 , resize = True )
