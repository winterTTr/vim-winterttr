import vim

from pyVim.pvWrap import pvWindow , pvWinSplitter

from pyVim.pvKeyMap import pvKeyMapEvent , pvKeyMapManager , pvKeyMapObserver
from pyVim.pvKeyMap import PV_KM_MODE_NORMAL 

class Application( pvKeyMapObserver ):
    def __init__( self ):
        self.__key_event = []
        self.__key_event.append( pvKeyMapEvent( "<M-1>" , PV_KM_MODE_NORMAL ) )
        self.__key_event.append( pvKeyMapEvent( "<M-2>" , PV_KM_MODE_NORMAL ) )

        self.__ui = {}
        # info about "TabExplorer"
        self.__ui['TabExplorer'] = {}
        self.__ui['TabExplorer']['window'] = None
        self.__ui['TabExplorer']['buffer'] = None
        # info about "FileExplorer"
        self.__ui['FileExplorer'] = {}
        self.__ui['FileExplorer']['window'] = None
        self.__ui['FileExplorer']['buffer'] = None

        vim.command('nnoremenu <silent> pyfiles.\ pvExPanelMode :py pvExPanelMode.app.start()<CR>')

    def start( self ):
        for event in self.__key_event:
            pvKeyMapManager.registerObserver( event , self )
        vim.command('nunmenu pyfiles.\ pvExPanelMode')
        vim.command('nnoremenu <silent> pyfiles.*pvExPanelMode :py pvExPanelMode.app.stop()<CR>')

    def stop( self ):
        if self.__ui['TabExplorer']['buffer']:
            # destroy buffer
            self.__ui['TabExplorer']['buffer'].destroy()
            self.__ui['TabExplorer']['buffer'] = None

            # close(destroy) window
            self.__ui['TabExplorer']['window'].closeWindow()
            self.__ui['TabExplorer']['window'] = None

        if self.__ui['FileExplorer']['buffer']:
            # destroy buffer
            self.__ui['FileExplorer']['buffer'].destroy()
            self.__ui['FileExplorer']['buffer'] = None

            # close(destroy) window
            self.__ui['FileExplorer']['window'].closeWindow()
            self.__ui['FileExplorer']['window'] = None

        for event in self.__key_event:
            pvKeyMapManager.removeObserver( event , self )

        vim.command('nunmenu pyfiles.*pvExPanelMode')
        vim.command('nnoremenu <silent> pyfiles.\ pvExPanelMode :py pvExPanelMode.app.start()<CR>')

    def switchTabExplorer( self ):
        if_window_open = False
        if self.__ui['TabExplorer']['buffer']:
            if_window_open = self.__ui['TabExplorer']['window'].isShown()

            # destroy buffer
            self.__ui['TabExplorer']['buffer'].destroy()
            self.__ui['TabExplorer']['buffer'] = None

            # close(destroy) window
            self.__ui['TabExplorer']['window'].closeWindow()
            self.__ui['TabExplorer']['window'] = None

        if if_window_open : return

        _target_win = pvWindow()
        # split window
        from pyVim.pvWrap import PV_SPLIT_TYPE_CUR_BOTTOM
        self.__ui['TabExplorer']['window'] = pvWinSplitter( PV_SPLIT_TYPE_CUR_BOTTOM , ( -1 , 1 ) , _target_win ).doSplit()

        from pveBufferExplorer import TabbedBufferExplorer
        self.__ui['TabExplorer']['buffer'] = TabbedBufferExplorer( _target_win )
        self.__ui['TabExplorer']['buffer'].showBuffer( self.__ui['TabExplorer']['window'] )

    def switchFileExplorer( self ):
        if_window_open = False
        if self.__ui['FileExplorer']['buffer']:
            if_window_open = self.__ui['FileExplorer']['window'].isShown()

            # destroy buffer
            self.__ui['FileExplorer']['buffer'].destroy()
            self.__ui['FileExplorer']['buffer'] = None

            # close(destroy) window
            self.__ui['FileExplorer']['window'].closeWindow()
            self.__ui['FileExplorer']['window'] = None

        if if_window_open : return

        _target_win = pvWindow()
        # split window
        from pyVim.pvWrap import PV_SPLIT_TYPE_MOST_LEFT
        self.__ui['FileExplorer']['window'] = pvWinSplitter( PV_SPLIT_TYPE_MOST_LEFT , ( 25 , -1 ) ).doSplit()

        from pveFileExplorer import FileExplorer
        self.__ui['FileExplorer']['buffer'] = FileExplorer( _target_win )
        self.__ui['FileExplorer']['buffer'].showBuffer( self.__ui['FileExplorer']['window'] )



    def OnHandleKeyEvent( self , **kwdict ):
        if kwdict['key'] == "<M-1>":
            self.switchTabExplorer()
        elif kwdict['key'] == "<M-2>":
            self.switchFileExplorer()
