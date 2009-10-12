from pyVim.pvExBuffer import pvListBuffer
from pyVim.pvTabPanel import pvTabPanelItem

class exVimPanel_ContextComplete( pvTabPanelItem ):
    def __init__( self ):
        self.buffer = pvListBuffer()

    def getBuffer( self ):
        return self.buffer

    def __str__( self ):
        return 'context complete'

