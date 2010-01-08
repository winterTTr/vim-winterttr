from pyvim.pvListBuffer import pvListBuffer , pvListBufferObserver

class PanelSwitcher(pvListBufferObserver):
    def __init__( self , list_buffer ):
        list_buffer.registerObserver( self )
        self.ob_list = []

    def OnSelectItemChanged( self , item ):
        for x in self.ob_list:
            x.OnPanelSelected( item )


class PanelManager(object):
    def __init__( self , win_mgr ):
        self.win_mgr = win_mgr

        # init the buffer show in 'caption window'
        self.buffer = pvListBuffer()
        self.buffer.showBuffer( self.win_mgr.getWindow('list') )
        self.buffer.updateBuffer( format = '< %-20s >' , hilight = 'Visual' , resize = True )

        self.ps = PanelSwitcher( self.buffer )

    def loadPanels( self ):
        import pvePanels 
        for panel in pvePanels.load_panels:
            _module = __import__( 'pvePanels.%s' % panel , globals() , locals() , ['_class_'] )
            _object = _module._class_( self.win_mgr )
            self.ps.ob_list.append( _object )
            self.buffer.items.append( _object.name )
        self.buffer.updateBuffer()





