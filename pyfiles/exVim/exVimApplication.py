from pyVim.pvWrap import pvWindowManager
from pyVim.pvExBuffer import pvListBuffer

from pyVim.pvKeyMapManager import pvKeyMapManager
from pyVim.pvKeyMapManager import PV_KMM_MODE_INSERT , PV_KMM_MODE_NORMAL


exVim_key_map_manager = pvKeyMapManager()
exVim_window_manager = pvWindowManager()

class Application:
    def __init__( self ):
        self.panels_caption = ['complete' , 'buffer list' , 'file explorer' ]
        self.panels = [ pvListBuffer() , pvListBuffer() , pvListBuffer() ]
        self.list_panel = pvListBuffer()
        #self.keymgr.register( '<C-J>' , PV_KMM_MODE_INSERT , M.do_key )
        #self.keymgr.register( '<C-K>' , PV_KMM_MODE_INSERT , M.do_key )

    def start( self ):
        exVim_window_manager.makeWindows('(-,-)main | ( 30 , - )panel , ( -,10) list')

        defaul_selection = 0 
        self.list_panel.showBuffer( exVim_window_manager.getWindow('list') )
        self.list_panel.data = self.panels_caption
        self.list_panel.updateBuffer( selection = defaul_selection , resize = True )

        self.panels[defaul_selection].showBuffer( exVim_window_manager.getWindow('panel') )
        self.panels[defaul_selection].data = [ '11' , '22' , '33' ]
        self.panels[defaul_selection].updateBuffer( selection = 0 )


        
