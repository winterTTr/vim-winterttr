import vim
from pyVim.pvWrap import pvWindowManager 

class Application:
    def __init__( self ):
        self.wm = pvWindowManager()

    #def initMagicKey( self ):
    #    vim.command( 'set noshowmode' )
    #    self.magic_key_list = []

    #    from pveMagicKey import pveKey_ExpandContent
    #    self.magic_key_list.append( pveKey_ExpandContent( self.wm.getWindow('main') ) )

    #    from pveMagicKey import pveKey_AutoAddPair
    #    self.magic_key_list.append( pveKey_AutoAddPair( self.wm.getWindow('main') ) )

    #    from pveMagicKey import pveKey_AutoMoveRightPair
    #    self.magic_key_list.append( pveKey_AutoMoveRightPair( self.wm.getWindow('main') ) )

    #    from pveMagicKey import pveKey_ChangeSelectionOnPanel
    #    self.magic_key_list.append( pveKey_ChangeSelectionOnPanel(self.tp) )

    #    from pveMagicKey import pveKey_ChangeSelectonOnPanelList
    #    self.magic_key_list.append( pveKey_ChangeSelectonOnPanelList(self.tp) )

    #    from pveMagicKey import pveKey_AutoContextComplete
    #    self.magic_key_list.append( pveKey_AutoContextComplete( self.wm.getWindow('main') , self.tp) )

    #    from pveMagicKey import pveKey_AcceptSelectionOnPanel
    #    self.magic_key_list.append( pveKey_AcceptSelectionOnPanel( self.wm.getWindow('main') , self.tp) )

    #    from pveMagicKey import pveKey_OpenTreeItem
    #    self.magic_key_list.append( pveKey_OpenTreeItem( self.tp ) )

    #    for key in self.magic_key_list :
    #        key.register()


    def start( self ):
        self.wm.makeWindows('( 25 , - )panel , ( -,10) list | (-,-)main , ( - , 10 )cmd')

        from pvePanelLoader import PanelManager
        self.pm = PanelManager( self.wm )
        self.pm.loadPanels()

        #from pveFunctionPanel import pvePanel_ContextComplete , pvePanel_BufferExplorer , pvePanel_FileExplorer
        #self.tp.addPanel( pvePanel_ContextComplete() )
        #self.tp.addPanel( pvePanel_BufferExplorer() )
        #self.tp.addPanel( pvePanel_FileExplorer() )
        #self.initMagicKey()

