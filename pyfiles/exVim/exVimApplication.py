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
        self.panel_list = pvListBuffer()

        exVim_key_map_manager.register( '<C-J>' , PV_KMM_MODE_INSERT , self.moveItem_Panel )
        exVim_key_map_manager.register( '<C-J>' , PV_KMM_MODE_NORMAL , self.moveItem_Panel )
        exVim_key_map_manager.register( '<C-K>' , PV_KMM_MODE_INSERT , self.moveItem_Panel )
        exVim_key_map_manager.register( '<C-K>' , PV_KMM_MODE_NORMAL , self.moveItem_Panel )

        exVim_key_map_manager.register( '<M-j>' , PV_KMM_MODE_NORMAL , self.moveItem_List )
        exVim_key_map_manager.register( '<M-j>' , PV_KMM_MODE_INSERT , self.moveItem_List )
        exVim_key_map_manager.register( '<M-k>' , PV_KMM_MODE_NORMAL , self.moveItem_List )
        exVim_key_map_manager.register( '<M-k>' , PV_KMM_MODE_INSERT , self.moveItem_List )

    def start( self ):
        exVim_window_manager.makeWindows('(-,-)main | ( 30 , - )panel , ( -,10) list')

        defaul_selection = 0 
        self.panel_list.showBuffer( exVim_window_manager.getWindow('list') )
        self.panel_list.data = self.panels_caption
        self.panel_list.updateBuffer( selection = defaul_selection , resize = True )

        self.panels[defaul_selection].showBuffer( exVim_window_manager.getWindow('panel') )
        self.panels[defaul_selection].data = [ '11' , '22' , '33' ]
        self.panels[defaul_selection].updateBuffer( selection = 0 )


    def moveItem_Panel( self , keyname , mode ):
        buffer = self.panels[ self.panel_list.selection ]
        if isinstance( buffer , pvListBuffer ):
            buffer.updateSelection( 1 if keyname == "<C-J>" else -1 )


    def moveItem_List( self , keyname , mode ):
        self.panel_list.updateSelection( 1 if keyname == "<M-j>" else -1 )

        buffer_to_show = self.panels[ self.panel_list.selection ]
        buffer_to_show.showBuffer( exVim_window_manager.getWindow('panel') )
        buffer_to_show.updateBuffer()



        

        

        
