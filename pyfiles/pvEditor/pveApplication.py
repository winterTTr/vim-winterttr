import vim
from pyVim.pvWrap import pvWindowManager 

from pyVim.pvKeyMap import pvKeyMapEvent , pvKeyMapManager , pvKeyMapObserver
from pyVim.pvKeyMap import PV_KM_MODE_NORMAL 

class Application( pvKeyMapManager ):
    def __init__( self ):
        self.wm = pvWindowManager()

    def start( self ):
        self.wm.makeWindows('( 25 , 10 ) list , ( 25 , - )panel | (-,-)main')

        from pvePanelLoader import PanelManager
        self.pm = PanelManager( self.wm )
        self.pm.loadPanels()
        
        move_list_event = pvKeyMapEvent( "<M-1>" , PV_KM_MODE_NORMAL )
        pvKeyMapManager.registerObserver( move_list_event , self)

        move_panel_event = pvKeyMapEvent( "<M-2>" , PV_KM_MODE_NORMAL )
        pvKeyMapManager.registerObserver( move_panel_event , self )

        move_main_event = pvKeyMapEvent( "<M-3>" , PV_KM_MODE_NORMAL )
        pvKeyMapManager.registerObserver( move_main_event , self )


    def OnHandleKeyEvent( self , **kwdict ):
        if kwdict['key'] == "<M-1>":
            self.wm.getWindow('list').setFocus()
        elif kwdict['key'] == "<M-2>":
            self.wm.getWindow('panel').setFocus()
        elif kwdict['key'] == "<M-3>":
            self.wm.getWindow('main').setFocus()
