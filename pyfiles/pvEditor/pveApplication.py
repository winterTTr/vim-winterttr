import vim
from pyVim.pvWrap import pvWindowManager 

class Application:
    def __init__( self ):
        self.wm = pvWindowManager()

    def start( self ):
        self.wm.makeWindows('( 25 , 10 ) list , ( 25 , - )panel | (-,-)main')

        from pvePanelLoader import PanelManager
        self.pm = PanelManager( self.wm )
        self.pm.loadPanels()

