import vim
from pvEditorTabPanel import pvEditorTabPanelManager
from pyVim.pvWrap import pvWindowManager 
from pyVim.pvKeyMap import pvKeyMapManager

class Application:
    def __init__( self ):
        self.wm = pvWindowManager()

    def initMagicKey( self ):
        vim.command( 'set noshowmode' )
        self.magic_key_list = []

        from pvEditorMagicKey import pvEditorKey_ExpandContent
        self.magic_key_list.append( pvEditorKey_ExpandContent( self.wm.getWindow('main') ) )

        from pvEditorMagicKey import pvEditorKey_AutoAddPair
        self.magic_key_list.append( pvEditorKey_AutoAddPair( self.wm.getWindow('main') ) )

        from pvEditorMagicKey import pvEditorKey_AutoMoveRightPair
        self.magic_key_list.append( pvEditorKey_AutoMoveRightPair( self.wm.getWindow('main') ) )

        from pvEditorMagicKey import pvEditorKey_ChangeSelectionOnPanel
        self.magic_key_list.append( pvEditorKey_ChangeSelectionOnPanel(self.tp) )

        from pvEditorMagicKey import pvEditorKey_ChangeSelectonOnPanelList
        self.magic_key_list.append( pvEditorKey_ChangeSelectonOnPanelList(self.tp) )

        from pvEditorMagicKey import pvEditorKey_AutoContextComplete
        self.magic_key_list.append( pvEditorKey_AutoContextComplete( self.wm.getWindow('main') , self.tp) )

        from pvEditorMagicKey import pvEditorKey_AcceptSelectionOnPanel
        self.magic_key_list.append( pvEditorKey_AcceptSelectionOnPanel( self.wm.getWindow('main') , self.tp) )

        from pvEditorMagicKey import pvEditorKey_OpenTreeItem
        self.magic_key_list.append( pvEditorKey_OpenTreeItem( self.tp ) )

        for key in self.magic_key_list :
            key.register()


    def start( self ):
        self.wm.makeWindows('( 25 , - )panel , ( -,10) list | (-,-)main ')
        self.tp = pvEditorTabPanelManager( 
                self.wm.getWindow('list') ,
                self.wm.getWindow('panel') )

        from pvEditorFunctionPanel import pvEditorPanel_ContextComplete , pvEditorPanel_BufferExplorer , pvEditorPanel_FileExplorer
        self.tp.addPanel( pvEditorPanel_ContextComplete() )
        self.tp.addPanel( pvEditorPanel_BufferExplorer() )
        self.tp.addPanel( pvEditorPanel_FileExplorer() )
        self.initMagicKey()

