from pyVim.pvWrap import pvWindowManager
from pyVim.pvExBuffer import pvListBuffer

from pyVim.pvKeyMapManager import pvKeyMapManager
from pyVim.pvKeyMapManager import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL

class Application:
    def __init__( self ):
        self.winmgr = pvWindowManager()
        self.keymgr = pvKeyMapManager()

        #self.keymgr.register( '<C-J>' , PV_KMM_MODE_INSERT , M.do_key )
        #self.keymgr.register( '<C-K>' , PV_KMM_MODE_INSERT , M.do_key )

    def start( self ):
        self.winmgr.makeWindows('(-,-)main | ( 30 , - )panel , ( -,10) list')

        self.tabnamelist = pvListBuffer()
        self.tabnamelist.showBuffer( self.winmgr.getWindow('list') )

        self.tabnamelist.data = ['complete' , 'buffer list' , 'file explorer' , '123' ]
        self.tabnamelist.updateBuffer( selection = 1 , resize = True )


        
