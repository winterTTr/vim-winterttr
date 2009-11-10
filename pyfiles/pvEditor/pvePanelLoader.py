from pyVim.pvListBuffer import pvListBuffer , pvListBufferObserver


class PanelManager(object):
    def __init__( self , win_mgr ):
        self.win_mgr = win_mgr

        # init the buffer show in 'caption window'
        self.buffer = pvListBuffer()
        self.buffer.showBuffer( self.win_mgr.getWindow('list') )
        self.buffer.updateBuffer( format = '< %-20s >' , hilight = 'Visual' , resize = True )

    def loadPanels( self ):
        import pvePanels 
        for panel in pvePanels.load_panels:
            _module = __import__( 'pvePanels.%s' % panel , globals() , locals() , ['_class_'] )
            _object = _module._class_( self.win_mgr )
            self.buffer.registerObserver( _object )
            self.buffer.items.append( _object.name )
            self.buffer.updateBuffer()






