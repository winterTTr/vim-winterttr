import vim
from pyVim.pvWrap import pvWindowManager 
from pyVim.pvKeyMap import pvKeyMapManager
from pyVim.pvTabPanel import pvTabPanelManager

class Application:
    def __init__( self ):
        self.wm = pvWindowManager()

    def initMagicKey( self ):
        vim.command( 'set noshowmode' )
        self.magic_key_list = []

        from exVimMagicKey import exVimKey_ExpandContent
        self.magic_key_list.append( exVimKey_ExpandContent( self.wm.getWindow('main') ) )

        from exVimMagicKey import exVimKey_AutoAddPair
        self.magic_key_list.append( exVimKey_AutoAddPair( self.wm.getWindow('main') ) )

        from exVimMagicKey import exVimKey_AutoMoveRightPair
        self.magic_key_list.append( exVimKey_AutoMoveRightPair( self.wm.getWindow('main') ) )

        from exVimMagicKey import exVimKey_ChangeSelectionOnPanel
        self.magic_key_list.append( exVimKey_ChangeSelectionOnPanel(self.tp) )

        from exVimMagicKey import exVimKey_ChangeSelectonOnPanelList
        self.magic_key_list.append( exVimKey_ChangeSelectonOnPanelList(self.tp) )

        from exVimMagicKey import exVimKey_AutoContextComplete
        self.magic_key_list.append( exVimKey_AutoContextComplete( self.wm.getWindow('main') , self.tp) )

        from exVimMagicKey import exVimKey_AcceptSelectionOnPanel
        self.magic_key_list.append( exVimKey_AcceptSelectionOnPanel( self.wm.getWindow('main') , self.tp) )

        from exVimMagicKey import exVimKey_OpenTreeItem
        self.magic_key_list.append( exVimKey_OpenTreeItem( self.tp ) )

        for key in self.magic_key_list :
            key.register()


    def start( self ):
        self.wm.makeWindows('( 25 , - )panel , ( -,10) list | (-,-)main ')
        self.tp = pvTabPanelManager( 
                self.wm.getWindow('list') ,
                self.wm.getWindow('panel') )

        from exVimFunctionPanel import exVimPanel_ContextComplete , exVimPanel_BufferExplorer , exVimPanel_FileExplorer
        self.tp.addPanel( exVimPanel_ContextComplete() )
        self.tp.addPanel( exVimPanel_BufferExplorer() )
        self.tp.addPanel( exVimPanel_FileExplorer() )
        self.initMagicKey()

